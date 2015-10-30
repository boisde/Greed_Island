# -*- coding:utf-8 -*-

import json
import traceback

from rest_framework.status import *
from django.views.generic.base import View
from django.db.models import ForeignKey, DateTimeField
from django.core.exceptions import ObjectDoesNotExist

from tools_lib.response import JsonResponse, ErrorResponse
from tools_lib.pagination import paginator
from tools_lib.exception import InvalidParams, ServiceError
from tools_lib.gedis.gedis import Redis
from tools_lib.timezone import TimeZone
from tools_lib.decorator import class_authenticated


class BaseAPIView(View):
    def __init__(self):
        self.http_request, self.http_args, self.http_kwargs = None, None, None
        self.redis_client = Redis()
        self.http_method_names.append('patch')
        super(BaseAPIView, self).__init__()

    def dispatch(self, request, *args, **kwargs):
        self.http_request, self.http_args, self.http_kwargs = request, args, kwargs
        return super(BaseAPIView, self).dispatch(request, *args, **kwargs)


class SerializerMixin(object):
    model = None
    serialize_fields = []
    exclude_serialize_fields = []

    def __init__(self):
        super(SerializerMixin, self).__init__()

    def serialize(self, instance):
        if hasattr(instance, 'info'):
            return instance.info()

        result = {}
        field_names = map(lambda x: x.name, self.model._meta.fields)
        reversed_field = {x.name: x for x in self.model._meta.fields}
        if self.serialize_fields:
            field_names = set(field_names) & set(self.serialize_fields)
        if self.exclude_serialize_fields:
            field_names = set(field_names) - set(self.exclude_serialize_fields)
        for f_name in field_names:
            if type(reversed_field[f_name]) == ForeignKey:
                # the foreignkey field may be None
                result[f_name] = getattr(instance, f_name).pk if getattr(instance, f_name) else None
            # 特殊处理时间类型字段
            elif type(reversed_field[f_name]) == DateTimeField:
                result[f_name] = TimeZone.datetime_to_str(getattr(instance, f_name))
            else:
                result[f_name] = getattr(instance, f_name)

        return result

    def restore_object(self, attrs, instance=None):
        if instance:
            # update existing instance
            fields = filter(lambda x: x.name != 'id', self.model._meta.fields)
            for field in fields:
                if field.name in attrs:
                    if type(field) == ForeignKey:
                        # field may be None
                        try:
                            related_instance = field.related.parent_model.objects.get(pk=int(attrs[field.name]))
                        except Exception:
                            print traceback.format_exc()
                            related_instance = None
                        setattr(instance, field.name, related_instance)
                    # 特殊处理时间类型字段
                    elif type(field) == DateTimeField and type(attrs[field.name]) == unicode:
                        setattr(instance, field.name, TimeZone.str_to_datetime(attrs[field.name]))
                    else:
                        setattr(instance, field.name, attrs[field.name])
            return instance
        # return a new model instance
        else:
            kwargs = {}
            fields = filter(lambda x: x.name != 'id', self.model._meta.fields)
            for field in fields:
                if field.name in attrs:
                    if type(field) == ForeignKey:
                        # field may be None
                        try:
                            related_instance = field.related.parent_model.objects.get(pk=int(attrs[field.name]))
                        except Exception:
                            print traceback.format_exc()
                            related_instance = None
                        kwargs[field.name] = related_instance
                    # 特殊处理时间类型字段
                    elif type(field) == DateTimeField and type(attrs[field.name]) == unicode:
                        setattr(instance, field.name, TimeZone.str_to_datetime(attrs[field.name]))
                    else:
                        kwargs[field.name] = attrs[field.name]
        return self.model._default_manager.create(**kwargs)


class ContextMixin(object):
    model = None
    extra_param = []

    def __init__(self):
        super(ContextMixin, self).__init__()
        # 易变的实例属性
        self.custom_kwargs = {}
        self.__context_data = {}
        self.__http_accept = {}

    # 必须在pre_XXX hook函数之后调用, 否则可能在pre_XXX hook函数中增加自定义参数会失效
    def get_context_data(self, request, *args, **kwargs):
        if self.__context_data:
            return self.__context_data
        kwargs = dict()

        if request.method == 'GET':
            data = request.GET
            kwargs['count'] = data.get('count', 10)
            kwargs['page'] = data.get('page', 1)
            kwargs['cursor'] = data.get('cursor')
        else:
            try:
                data = json.loads(request.body)
                field_names = map(lambda x: x.name, self.model._meta.fields)
                for f_name in field_names:
                    if f_name in data:
                        kwargs[f_name] = data.get(f_name)
            except Exception:
                print traceback.format_exc()
                raise InvalidParams(HTTP_400_BAD_REQUEST, 'invalid parameters')
        # 额外的参数，不论任何类型的HTTP方法都要处理
        for extra_p in self.extra_param:
            if extra_p in data:
                kwargs[extra_p] = data.get(extra_p)
        kwargs.update(self.custom_kwargs)
        self.__context_data = kwargs
        return kwargs

    # 解析HTTP_ACCEPT
    def parse_accept(self, request):
        if self.__http_accept:
            return self.__http_accept
        result = dict()
        accept = request.META.get('HTTP_ACCEPT')
        if accept:
            _accept = accept.split(';')
            for x in _accept:
                if '=' in x:
                    result[x.split('=')[0]] = x.split('=')[1]
        # 默认 version = 1
        if 'version' not in result.keys():
            result['version'] = 1
        self.__http_accept = result
        return self.__http_accept


class SingleObjectMixin(object):
    model = None
    pk_key_name = 'pk'
    has_deleted = True

    def __init__(self):
        super(SingleObjectMixin, self).__init__()
        # 易变的实例属性
        self.pk = None
        self.filter_args = []
        self.filter_kwargs = {}
        if self.has_deleted:
            self.filter_kwargs.update({'deleted': False})

    def get_object(self, **kwargs):
        self.pk = self.pk if self.pk else kwargs[kwargs[self.pk_key_name]]
        lookup_kwargs = {}
        lookup_kwargs.update(self.filter_kwargs)
        lookup_kwargs.update({
            'pk': self.pk if self.pk else kwargs[kwargs[self.pk_key_name]]
        })
        if self.model:
            return self.model._default_manager.get(*self.filter_args, **lookup_kwargs)
        else:
            raise Exception("%(cls)s has not define model" % {'cls': self.__class__.__name__})


class MultipleObjectsMixin(object):
    model = None
    order_by = '-create_time'
    has_deleted = True

    def __init__(self):
        super(MultipleObjectsMixin, self).__init__()
        # 易变的实例属性
        self.filter_args = []
        self.exclude_kwargs = {}
        self.filter_kwargs = {}
        if self.has_deleted:
            self.filter_kwargs.update({'deleted': False})

    def get_queryset(self, request, *args, **kwargs):
        lookup_kwargs = {}
        lookup_kwargs.update(self.filter_kwargs)
        if self.model:
            result = self.model._default_manager.filter(*self.filter_args, **lookup_kwargs).exclude(**self.exclude_kwargs)
            if self.order_by:
                result = result.order_by(self.order_by)
            return result
        else:
            raise Exception("%(cls)s has not define model" % {'cls': self.__class__.__name__})


class PagingMixin(ContextMixin):
    def __init__(self):
        super(PagingMixin, self).__init__()

    def paging(self, request, iterable_objects):
        context = self.get_context_data(request)
        cursor = context.get('cursor')
        page = context.get('page')
        count = context.get('count')
        rst = paginator(request, iterable_objects, lambda x: x.id, cursor=cursor, page=page, count=count)
        return rst[0], rst[1], rst[2]


class RetrieveModelMixin(SingleObjectMixin, SerializerMixin, ContextMixin):
    def __init__(self):
        super(RetrieveModelMixin, self).__init__()

    def pre_get(self, request, *args, **kwargs):
        pass

    def post_get(self, request, *args, **kwargs):
        pass

    def retrieve(self, request, *args, **kwargs):
        if hasattr(self, 'pre_get'):
            getattr(self, 'pre_get')(request, *args, **kwargs)
        obj = None
        try:
            obj = self.get_object(**kwargs)
            return JsonResponse(data=self.serialize(obj), status_code=HTTP_200_OK)
        except ObjectDoesNotExist:
            print traceback.format_exc()
            return ErrorResponse(msg='ObjectDoesNotExist: %d' % self.pk)
        finally:
            if hasattr(self, 'post_get'):
                getattr(self, 'post_get')(request, obj, *args, **kwargs)


class CreateModelMixin(ContextMixin, SerializerMixin):
    def __init__(self):
        super(CreateModelMixin, self).__init__()

    def pre_save(self, request, *args, **kwargs):
        pass

    def post_save(self, instance=None, context_data=None):
        pass

    def create(self, request, *args, **kwargs):
        if hasattr(self, 'pre_save'):
            getattr(self, 'pre_save')(request, *args, **kwargs)
        attrs = self.get_context_data(request, *args, **kwargs)
        new_obj = self.restore_object(attrs)
        if hasattr(self, 'post_save'):
            getattr(self, 'post_save')(instance=new_obj, context_data=attrs)
        return JsonResponse(data=self.serialize(new_obj), status_code=HTTP_201_CREATED)


class ListModelMixin(PagingMixin, MultipleObjectsMixin, SerializerMixin):
    def __init__(self):
        super(ListModelMixin, self).__init__()

    def pre_get(self, request, *args, **kwargs):
        pass

    def post_get(self, request, *args, **kwargs):
        pass

    def list(self, request, *args, **kwargs):
        if hasattr(self, 'pre_get'):
            getattr(self, 'pre_get')(request, *args, **kwargs)

        query_set = self.get_queryset(request, *args, **kwargs)

        if hasattr(self, 'post_get'):
            getattr(self, 'post_get')(request, *args, **kwargs)

        content, resource_count, link = self.paging(request, query_set)
        response = JsonResponse(data=[self.serialize(x) for x in content], status_code=HTTP_200_OK)
        response['X-Resource-Count'] = resource_count
        response['Link'] = link
        return response


class UpdateModelMixin(SingleObjectMixin, SerializerMixin, ContextMixin):
    def __init__(self):
        super(UpdateModelMixin, self).__init__()

    def pre_save(self, request, *args, **kwargs):
        pass

    def post_save(self, instance=None, context_data=None):
        pass

    def update(self, request, *args, **kwargs):
        if hasattr(self, 'pre_save'):
            getattr(self, 'pre_save')(request, *args, **kwargs)
        obj = self.get_object(**kwargs)
        attrs = self.get_context_data(request, *args, **kwargs)
        obj = self.restore_object(attrs, instance=obj)
        obj.save()
        if hasattr(self, 'post_save'):
            getattr(self, 'post_save')(instance=obj, context_data=attrs)
        return JsonResponse(data=self.serialize(obj), status_code=HTTP_201_CREATED)


class DestroyModelMixin(SingleObjectMixin):
    def __init__(self):
        super(DestroyModelMixin, self).__init__()

    fake_delete = True

    def pre_delete(self, request, *args, **kwargs):
        pass

    def post_delete(self, request, *args, **kwargs):
        pass

    def destroy(self, request, *args, **kwargs):
        if hasattr(self, 'pre_delete'):
            getattr(self, 'pre_delete')(request, *args, **kwargs)
        obj = self.get_object(**kwargs)
        if self.fake_delete and hasattr(obj, 'deleted'):
            obj.deleted = True
            obj.save()
        else:
            obj.mark_deleted()
        if hasattr(self, 'post_delete'):
            getattr(self, 'post_delete')(request, *args, **kwargs)
        return JsonResponse(status_code=HTTP_204_NO_CONTENT)


###################################################################
# Concrete View Classes

class CreateAPIView(CreateModelMixin, BaseAPIView):
    def __init__(self):
        super(CreateAPIView, self).__init__()

    @class_authenticated
    def post(self, request, *args, **kwargs):
        try:
            return self.create(request, *args, **kwargs)
        except InvalidParams, e:
            print e[1]
            return ErrorResponse(msg=e[1], status_code=e[0])
        except ServiceError, e:
            print e[1]
            return ErrorResponse(msg=e[1], status_code=e[0])
        except Exception, e:
            print traceback.format_exc()
            return ErrorResponse(msg=str(e))


class ListAPIView(ListModelMixin, BaseAPIView):
    def __init__(self):
        super(ListAPIView, self).__init__()

    @class_authenticated
    def get(self, request, *args, **kwargs):
        try:
            return self.list(request, *args, **kwargs)
        except InvalidParams, e:
            print e[1]
            return ErrorResponse(msg=e[1], status_code=e[0])
        except ServiceError, e:
            print e[1]
            return ErrorResponse(msg=e[1], status_code=e[0])
        except Exception, e:
            print traceback.format_exc()
            return ErrorResponse(msg=str(e))


class RetrieveAPIView(RetrieveModelMixin, BaseAPIView):
    def __init__(self):
        super(RetrieveAPIView, self).__init__()

    @class_authenticated
    def get(self, request, *args, **kwargs):
        try:
            return self.retrieve(request, *args, **kwargs)
        except InvalidParams, e:
            print e[1]
            return ErrorResponse(msg=e[1], status_code=e[0])
        except ServiceError, e:
            print e[1]
            return ErrorResponse(msg=e[1], status_code=e[0])
        except Exception, e:
            print traceback.format_exc()
            return ErrorResponse(msg=str(e))


class DestroyAPIView(DestroyModelMixin, BaseAPIView):
    def __init__(self):
        super(DestroyAPIView, self).__init__()

    @class_authenticated
    def delete(self, request, *args, **kwargs):
        try:
            return self.destroy(request, *args, **kwargs)
        except InvalidParams, e:
            print e[1]
            return ErrorResponse(msg=e[1], status_code=e[0])
        except ServiceError, e:
            print e[1]
            return ErrorResponse(msg=e[1], status_code=e[0])
        except Exception, e:
            print traceback.format_exc()
            return ErrorResponse(msg=str(e))


class UpdateAPIView(UpdateModelMixin, BaseAPIView):
    def __init__(self):
        super(UpdateAPIView, self).__init__()

    @class_authenticated
    def put(self, request, *args, **kwargs):
        try:
            return self.update(request, *args, **kwargs)
        except InvalidParams, e:
            print e[1]
            return ErrorResponse(msg=e[1], status_code=e[0])
        except ServiceError, e:
            print e[1]
            return ErrorResponse(msg=e[1], status_code=e[0])
        except Exception, e:
            print traceback.format_exc()
            return ErrorResponse(msg=str(e))

    @class_authenticated
    def patch(self, request, *args, **kwargs):
        try:
            return self.update(request, *args, **kwargs)
        except InvalidParams, e:
            print e[1]
            return ErrorResponse(msg=e[1], status_code=e[0])
        except ServiceError, e:
            print e[1]
            return ErrorResponse(msg=e[1], status_code=e[0])
        except Exception, e:
            print traceback.format_exc()
            return ErrorResponse(msg=str(e))


class ListCreateAPIView(ListModelMixin, CreateModelMixin, BaseAPIView):
    def __init__(self):
        super(ListCreateAPIView, self).__init__()

    @class_authenticated
    def get(self, request, *args, **kwargs):
        try:
            return self.list(request, *args, **kwargs)
        except InvalidParams, e:
            print e[1]
            return ErrorResponse(msg=e[1], status_code=e[0])
        except ServiceError, e:
            print e[1]
            return ErrorResponse(msg=e[1], status_code=e[0])
        except Exception, e:
            print traceback.format_exc()
            return ErrorResponse(msg=str(e))

    @class_authenticated
    def post(self, request, *args, **kwargs):
        try:
            return self.create(request, *args, **kwargs)
        except InvalidParams, e:
            print e[1]
            return ErrorResponse(msg=e[1], status_code=e[0])
        except ServiceError, e:
            print e[1]
            return ErrorResponse(msg=e[1], status_code=e[0])
        except Exception, e:
            print traceback.format_exc()
            return ErrorResponse(msg=str(e))


class RetrieveUpdateAPIView(RetrieveModelMixin, UpdateModelMixin, BaseAPIView):
    def __init__(self):
        super(RetrieveUpdateAPIView, self).__init__()

    @class_authenticated
    def get(self, request, *args, **kwargs):
        try:
            return self.retrieve(request, *args, **kwargs)
        except InvalidParams, e:
            print e[1]
            return ErrorResponse(msg=e[1], status_code=e[0])
        except ServiceError, e:
            print e[1]
            return ErrorResponse(msg=e[1], status_code=e[0])
        except Exception, e:
            print traceback.format_exc()
            return ErrorResponse(msg=str(e))

    @class_authenticated
    def put(self, request, *args, **kwargs):
        try:
            return self.update(request, *args, **kwargs)
        except InvalidParams, e:
            print e[1]
            return ErrorResponse(msg=e[1], status_code=e[0])
        except ServiceError, e:
            print e[1]
            return ErrorResponse(msg=e[1], status_code=e[0])
        except Exception, e:
            print traceback.format_exc()
            return ErrorResponse(msg=str(e))

    @class_authenticated
    def patch(self, request, *args, **kwargs):
        try:
            return self.update(request, *args, **kwargs)
        except InvalidParams, e:
            print e[1]
            return ErrorResponse(msg=e[1], status_code=e[0])
        except ServiceError, e:
            print e[1]
            return ErrorResponse(msg=e[1], status_code=e[0])
        except Exception, e:
            print traceback.format_exc()
            return ErrorResponse(msg=str(e))


class RetrieveDestroyAPIView(RetrieveModelMixin, DestroyModelMixin, BaseAPIView):
    def __init__(self):
        super(RetrieveDestroyAPIView, self).__init__()

    @class_authenticated
    def get(self, request, *args, **kwargs):
        try:
            return self.retrieve(request, *args, **kwargs)
        except InvalidParams, e:
            print e[1]
            return ErrorResponse(msg=e[1], status_code=e[0])
        except ServiceError, e:
            print e[1]
            return ErrorResponse(msg=e[1], status_code=e[0])
        except Exception, e:
            print traceback.format_exc()
            return ErrorResponse(msg=str(e))

    @class_authenticated
    def delete(self, request, *args, **kwargs):
        try:
            return self.destroy(request, *args, **kwargs)
        except InvalidParams, e:
            print e[1]
            return ErrorResponse(msg=e[1], status_code=e[0])
        except ServiceError, e:
            print e[1]
            return ErrorResponse(msg=e[1], status_code=e[0])
        except Exception, e:
            print traceback.format_exc()
            return ErrorResponse(msg=str(e))


class RetrieveUpdateDestroyAPIView(RetrieveModelMixin, UpdateModelMixin, DestroyModelMixin, BaseAPIView):
    def __init__(self):
        super(RetrieveUpdateDestroyAPIView, self).__init__()

    @class_authenticated
    def get(self, request, *args, **kwargs):
        try:
            return self.retrieve(request, *args, **kwargs)
        except InvalidParams, e:
            print e[1]
            return ErrorResponse(msg=e[1], status_code=e[0])
        except ServiceError, e:
            print e[1]
            return ErrorResponse(msg=e[1], status_code=e[0])
        except Exception, e:
            print traceback.format_exc()
            return ErrorResponse(msg=str(e))

    @class_authenticated
    def delete(self, request, *args, **kwargs):
        try:
            return self.destroy(request, *args, **kwargs)
        except InvalidParams, e:
            print e[1]
            return ErrorResponse(msg=e[1], status_code=e[0])
        except ServiceError, e:
            print e[1]
            return ErrorResponse(msg=e[1], status_code=e[0])
        except Exception, e:
            print traceback.format_exc()
            return ErrorResponse(msg=str(e))

    @class_authenticated
    def put(self, request, *args, **kwargs):
        try:
            return self.update(request, *args, **kwargs)
        except InvalidParams, e:
            print e[1]
            return ErrorResponse(msg=e[1], status_code=e[0])
        except ServiceError, e:
            print e[1]
            return ErrorResponse(msg=e[1], status_code=e[0])
        except Exception, e:
            print traceback.format_exc()
            return ErrorResponse(msg=str(e))

    @class_authenticated
    def patch(self, request, *args, **kwargs):
        try:
            return self.update(request, *args, **kwargs)
        except InvalidParams, e:
            print e[1]
            return ErrorResponse(msg=e[1], status_code=e[0])
        except ServiceError, e:
            print e[1]
            return ErrorResponse(msg=e[1], status_code=e[0])
        except Exception, e:
            print traceback.format_exc()
            return ErrorResponse(msg=str(e))


##########################################################
# 无token验证版本
class NoAuthListCreateAPIView(ListModelMixin, CreateModelMixin, BaseAPIView):
    def __init__(self):
        super(NoAuthListCreateAPIView, self).__init__()

    def get(self, request, *args, **kwargs):
        try:
            return self.list(request, *args, **kwargs)
        except InvalidParams, e:
            print e[1]
            return ErrorResponse(msg=e[1], status_code=e[0])
        except ServiceError, e:
            print e[1]
            return ErrorResponse(msg=e[1], status_code=e[0])
        except Exception, e:
            print traceback.format_exc()
            return ErrorResponse(msg=str(e))

    def post(self, request, *args, **kwargs):
        try:
            return self.create(request, *args, **kwargs)
        except InvalidParams, e:
            print e[1]
            return ErrorResponse(msg=e[1], status_code=e[0])
        except ServiceError, e:
            print e[1]
            return ErrorResponse(msg=e[1], status_code=e[0])
        except Exception, e:
            print traceback.format_exc()
            return ErrorResponse(msg=str(e))


class NoAuthCreateAPIView(CreateModelMixin, BaseAPIView):
    def __init__(self):
        super(NoAuthCreateAPIView, self).__init__()

    def post(self, request, *args, **kwargs):
        try:
            return self.create(request, *args, **kwargs)
        except InvalidParams, e:
            print e[1]
            return ErrorResponse(msg=e[1], status_code=e[0])
        except ServiceError, e:
            print e[1]
            return ErrorResponse(msg=e[1], status_code=e[0])
        except Exception, e:
            print traceback.format_exc()
            return ErrorResponse(msg=str(e))


class NoAuthListAPIView(ListModelMixin, BaseAPIView):
    def __init__(self):
        super(NoAuthListAPIView, self).__init__()

    def get(self, request, *args, **kwargs):
        try:
            return self.list(request, *args, **kwargs)
        except InvalidParams, e:
            print e[1]
            return ErrorResponse(msg=e[1], status_code=e[0])
        except ServiceError, e:
            print e[1]
            return ErrorResponse(msg=e[1], status_code=e[0])
        except Exception, e:
            print traceback.format_exc()
            return ErrorResponse(msg=str(e))


class NoAuthRetrieveUpdateDestroyAPIView(RetrieveModelMixin, UpdateModelMixin, DestroyModelMixin, BaseAPIView):
    def __init__(self):
        super(NoAuthRetrieveUpdateDestroyAPIView, self).__init__()

    def get(self, request, *args, **kwargs):
        try:
            return self.retrieve(request, *args, **kwargs)
        except InvalidParams, e:
            print e[1]
            return ErrorResponse(msg=e[1], status_code=e[0])
        except ServiceError, e:
            print e[1]
            return ErrorResponse(msg=e[1], status_code=e[0])
        except Exception, e:
            print traceback.format_exc()
            return ErrorResponse(msg=str(e))

    def delete(self, request, *args, **kwargs):
        try:
            return self.destroy(request, *args, **kwargs)
        except InvalidParams, e:
            print e[1]
            return ErrorResponse(msg=e[1], status_code=e[0])
        except ServiceError, e:
            print e[1]
            return ErrorResponse(msg=e[1], status_code=e[0])
        except Exception, e:
            print traceback.format_exc()
            return ErrorResponse(msg=str(e))

    def put(self, request, *args, **kwargs):
        try:
            return self.update(request, *args, **kwargs)
        except InvalidParams, e:
            print e[1]
            return ErrorResponse(msg=e[1], status_code=e[0])
        except ServiceError, e:
            print e[1]
            return ErrorResponse(msg=e[1], status_code=e[0])
        except Exception, e:
            print traceback.format_exc()
            return ErrorResponse(msg=str(e))

    def patch(self, request, *args, **kwargs):
        try:
            return self.update(request, *args, **kwargs)
        except InvalidParams, e:
            print e[1]
            return ErrorResponse(msg=e[1], status_code=e[0])
        except ServiceError, e:
            print e[1]
            return ErrorResponse(msg=e[1], status_code=e[0])
        except Exception, e:
            print traceback.format_exc()
            return ErrorResponse(msg=str(e))


class NoAuthRetrieveAPIView(RetrieveModelMixin, BaseAPIView):
    def __init__(self):
        super(NoAuthRetrieveAPIView, self).__init__()

    def get(self, request, *args, **kwargs):
        try:
            return self.retrieve(request, *args, **kwargs)
        except InvalidParams, e:
            print e[1]
            return ErrorResponse(msg=e[1], status_code=e[0])
        except ServiceError, e:
            print e[1]
            return ErrorResponse(msg=e[1], status_code=e[0])
        except Exception, e:
            print traceback.format_exc()
            return ErrorResponse(msg=str(e))
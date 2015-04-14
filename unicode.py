#!/usr/bin/env python
# encoding: utf-8
import os
import errno
import copy
import datetime


def ensure_dir(dir_name):
    """
    Ensure that a named directory exists; if it does not, attempt to create it.
    """
    try:
        if not dir_name.endswith('/'):
            dir_name += '/'
        os.makedirs(dir_name)
        os.chmod(dir_name, 0755)
    except OSError, e:
        if e.errno != errno.EEXIST:
            raise


def slice_dict(d, exclude_key):
    dd = {k: v for k, v in d.iteritems() if k is not exclude_key}
    return dd


def back_up(data):
    # C:\GCTI\Recording Processor\failed\<contactCenterDomain_tenantName_ccid>\recordingId_datetime.json
    failed_dir = os.path.join(os.getcwd(), "failed")
    tenant_dir = os.path.join(failed_dir, str("%s_%s_%s" % ('domain', 'tenant', 'ccid')))
    ensure_dir(tenant_dir)
    var = unicode('哈あdatetime', encoding='utf-8')
    now = datetime.datetime.now()
    metadata_file = "%s/%s_%s.%s.json" % (tenant_dir, 'recording_id', now.strftime('%Y%m%d-%H%M'), var)
    print type(metadata_file)
    try:
        with open(metadata_file, 'w') as the_metadata_file:
            # 如何正确的转化为unicode: decode('string_escape').decode('utf-8')
            unicode_data = str(data).decode('string_escape').decode('utf-8')
            the_metadata_file.write(unicode_data.encode('utf-8'))
    except EnvironmentError:
        print("Back up metadata record into [%s] failed." % the_metadata_file)
        return
    print("Back up metadata record into [%s] success." % the_metadata_file)

    with open(metadata_file, 'rb') as the_metadata_file:
        unicode_data = the_metadata_file.read().decode('utf_8')
        print("Decoded file: %s\n" % unicode_data.encode('utf_8'))

    """
    Test with copy.copy
    """
    data_copy = copy.copy(data)
    media = data_copy['mediaFiles'][0]
    media['parameters']['rp.speechminer_auth'] = '***:***'
    print("data=%s" % data)
    print("data_copy=%s\n" % data_copy)
    data_copy.pop("mediaFiles", None)
    print("data=%s" % data)
    print("data_copy=%s\n" % data_copy)

    """
    Test Exception
    """
    try:
        raise NameError("Hi NameError")
    except (NameError, EnvironmentError) as e:
        print(e)
    """
    Try dict slice
    """
    sliced_data = slice_dict(data, 'mediaFiles')
    print("[slice_dict()]sliced_data=%s" % sliced_data)

if __name__ == "__main__":

    # print os.listdir("/ds")
    back_up({
        "temporary_information": "temp",
        "mediaFiles":
            [
                {
                    "mediaDescriptor": {
                        "path": "x1.wav",
                        "storage": "awsS3",
                        "data": {
                            "bucket": "mybucket啦啦"
                        }
                    },
                    "startTime": "2012-12-18T13:45:032.000Z",
                    "stopTime": "2012-12-18T14:15:036.000Z",
                    "mediaId": "x1.wav",
                    "type": "audio/wav",
                    "duration": "534",
                    "tenant": "Environment",
                    "ivrprofile": "DéultIVRProfile",
                    "size": "8544",
                    "parameters": {
                        "sipsAppName": "sips1",
                        "record": "source",
                        "recorddn": "2222",
                        "callUuid": "x1",
                        "ani": "+14152213344",
                        "dnis": "+14155551234",
                        "agentdn": "2222",
                        "agentId": "agent1",
                        "rp.2": "x",
                        "rp.speechminer_auth": "default:password"
                    },
                    "masks": [
                        {"time": "2013-02-06T10:23:10.034Z", "type": "paused"},
                        {"time": "2013-02-06T10:23:23.124Z", "type": "resume"}
                    ],
                    "pkcs7": "...",
                    "certAlias": ["...", "..."]
                }
            ]
    })
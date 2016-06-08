void foo() {
  if (getOS().equals("MacOS")) {
    a();
  } else {
    b();
  }
  c();
  if (getOS().equals("MacOS")) {
    d();
  } else {
    e();
  }
}

void fooMacOS(){
    a();
    c();
    d();
}

void fooOther(){
    b();
    c();
    e();
}

void foo() {
  a();
  b()
  c();
  if (getOS().equals("MacOS")) {
    d();
  } else {
    e();
  }
}
void preFoo(){
    a();
    b();
    c();
}
void fooMacOS(){
    preFoo();
    d();
}
void fooOther(){
    preFoo();
    e();
}

class A {
    String x;

    void findX() {
        ...
        x = ...;
    }

    void foo() {
        findX();
        ...
        print(x);
    }
}

#include <node.h>
#include <string>

using namespace std;
namespace demo {

using v8::FunctionCallbackInfo;
using v8::Isolate;
using v8::Local;
using v8::Object;
using v8::String;
using v8::Value;


void Method(const FunctionCallbackInfo<Value>& args) {
  string huge = "";
  for(unsigned i = 0; i < 1000; ++i) huge += to_string(i) + "\n";
  const char * cHuge = huge.c_str();
  Isolate* isolate = args.GetIsolate();
  args.GetReturnValue().Set(String::NewFromUtf8(isolate, cHuge));
}

void init(Local<Object> exports) {
  NODE_SET_METHOD(exports, "sequential", Method);
}

NODE_MODULE(NODE_GYP_MODULE_NAME, init)

}

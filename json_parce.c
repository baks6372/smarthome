#include <json/json.h>
#include <stdio.h>

int main() {
  char * string = "{\"value\" : true,\"period\" : 5 ,\"dirtection\" : \"out\"}";
  printf("JSON string: %s\n", string);

  struct json_object *value, *period, *direction;
  json_object * jobj = json_tokener_parse(string);  

  json_object_object_get_ex(jobj, "value", &value);  
  json_object_object_get_ex(jobj, "period", &period);  
  json_object_object_get_ex(jobj, "dirtection", &direction);  

  printf("value = %s\n", json_object_to_json_string(value)); 
  printf("period = %s\n", json_object_to_json_string(period)); 
  printf("direction = %s\n", json_object_to_json_string(direction)); 
}

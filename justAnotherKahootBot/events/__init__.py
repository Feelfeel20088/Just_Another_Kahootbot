import importlib
import os
from pydantic import BaseModel
from typing import Dict, List, Tuple, Type, Set
from .bases import Event
import orjson
from justAnotherKahootBot.kahootBot.exceptions import UnknownJsonModelException
from collections import defaultdict
from justAnotherKahootBot.config.logger import logger


# ------------------------------------------------
#                      README
# ------------------------------------------------

# This code was written to handle a limitation in Kahoot's event system. 
# If Kahoot had included event IDs for their responses, much of this complexity 
# could have been avoided. Instead, we have to manually figure out what each response
# represents, which is why this code exists.
# 
# The primary goal of this script is to parse and handle Kahoot's event responses 
# and map them to the correct internal models, a task that would have been much 
# simpler with proper event identification from Kahoot.
# 
# If you're wondering why this exists, now you know.
# ------------------------------------------------
# TODO mabye use hashes instead with this. idk 

# Recursive function to get keys from JSON and fix kahoots json string inside json
def convert_ingress_json_keys_to_list(d: dict) -> List[str]:
   
    field_keys = []
    

    if not isinstance(d, dict):
        raise ValueError(f"when parsing json found {type(d)} instead of dict, please check if ingress json is a dict")
        
    for key, value in d.items():
        field_keys.append(key)
        if isinstance(value, dict):
            keys = convert_ingress_json_keys_to_list(value)
            field_keys.extend(keys) 
        # this is because some of the json that kahoot returns has json strings embedded in another json string.
        elif isinstance(value, str):
            try:
                maybe_json = orjson.loads(value)
                if isinstance(maybe_json, dict):
                    keys = convert_ingress_json_keys_to_list(maybe_json)
                    field_keys.extend(keys) 
                    
                    
            except orjson.JSONDecodeError:
                # logger.warning("Failed to parse embedded JSON string in key '%s'. The string is not valid JSON.", key)
                continue



    return field_keys





# Recursive function to get keys from Pydantic model
def convert_basemodel_keys_to_list(model: BaseModel) -> List[str]:
    
    field_keys = []
        
    for field_name, field in model.model_fields.items():
        
        field_keys.append(field_name)

        field_type = field.annotation
        

        if isinstance(field_type, type) and issubclass(field_type, BaseModel):
            # If the field is a subclass of BaseModel, recursively extract keys
            field_keys.extend(convert_basemodel_keys_to_list(field_type))
        

    
    return field_keys








event_classes: Dict[str, Dict[Type[BaseModel], Set[str]]] = defaultdict(dict)

def init_events():

    events_dir = os.path.dirname(__file__) 

    for root, _, files in os.walk(events_dir):

        for filename in files:

            if filename.endswith(".py") and filename != "__init__.py" and filename != "bases.py":
                file_location = os.path.relpath(os.path.join(root, filename), events_dir).replace("/", ".")
                module_location = f".{file_location[:-3]}"  
                

                module = importlib.import_module(module_location, package=__name__)

                for attr_name in dir(module):
                    
                    
                    attr = getattr(module, attr_name)
                    # TODO MAKE COMMONT HERE
                    if (
                        isinstance(attr, type) 
                        and issubclass(attr, BaseModel) 
                        and issubclass(attr, Event) 
                        and attr not in (BaseModel, Event)
                        and Event not in attr.__bases__
                    ):
                        logger.info(f"Loading event class {attr} into the map.")
                        if not "channel" in attr.model_fields:
                            logger.warning(f"warning: class {attr} does not have a channel type... skiping")
                            continue
                    
                        module_channel = attr.model_fields["channel"].default

                        event_classes[module_channel][attr] = set(convert_basemodel_keys_to_list(attr))
                        
                    
                
                    


debug_class_use_times: Dict[Type[BaseModel], int] = defaultdict(int)

async def compare_models_to_ingress_json(json: str, instance):
    # this lowers the time conplexity (o(n) - seperating the channles into diffrent lists)
    json = orjson.loads(json)
    json = json[0] # kahoot wraps json in a list

    # logger.info(orjson.dumps(json, option=orjson.OPT_INDENT_2).decode())
    
    channel = json["channel"]
    for model, model_keys in event_classes[channel].items():
        
        json_keys = set(convert_ingress_json_keys_to_list(json))
        
        # print("model keys: \n", model_keys, "\n json keys: \n", json_keys, "\n\n\n\n\n")
        if model_keys == json_keys:
            event = model.model_validate(json)
            debug_class_use_times[type(event)] += 1  
            await event.handle(instance)
            return
        
    logger.error(
        f"No suitable model to parse the provided JSON: {json}. "
        "If you're seeing this error, you might want to create an issue on GitHub "
        "or, even better, fix it yourself and submit a merge."
    )
    # raise UnknownJsonModelException(
    #     f"No suitable model to parse the provided JSON: {json}. "
    #     "If you're seeing this error, you might want to create an issue on GitHub "
    #     "or, even better, fix it yourself and submit a merge."
    # )

    




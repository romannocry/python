dataset_primary_key = "igg"
event_mapping_rules = { 
    'new_entry':{ 'label':'new joiner','actions':'newjoiner_actions'},
    'deleted_entry':{ 'label':'leaver','actions':'leaver_actions'},
    'rc':{ 'label':'mobility','actions':'mobility_actions'} 
}

dict_list_new = [
    {
        'igg': 100,
        'rc':'MSC1',
        'name':'Roman',
        'location':'Montreal'
    },
    {
        'igg': 101,
        'name':'John',
        'rc':'MSC1',
        'location':'NY'
    },
    {
        'igg': 103,
        'name':'Carry',
        'rc':'MSC1',
        'location':'Montreal'
    }
]
dict_list_old = [
    {
        'igg': 100,
        'name':'Roman',
        'rc':'MSC1',
        'location':'Montreal'
    },
    {
        'igg': 101,
        'name':'John',
        'rc':'MSC1',
        'location':'Montreal'
    },
    {
        'igg': 102,
        'name':'Brendan',
        'rc':'MSC1',
        'location':'Montreal'
    }
]

def dict_compare(d1, d2):
    d1_keys = set(d1.keys())
    d2_keys = set(d2.keys())
    intersect_keys = d1_keys.intersection(d2_keys)
    added = d1_keys - d2_keys
    removed = d2_keys - d1_keys
    modified = {o : (d1[o], d2[o]) for o in intersect_keys if d1[o] != d2[o]}
    same = set(o for o in intersect_keys if d1[o] == d2[o])
    return added, removed, modified, same

def dict_list_compare(primary_key,dl_new, dl_origin):
    event_list = []
    for i in range(len(dl_origin)):
        # Iterate through each key value pairs with the dictionnary (object)
        for key,value in dl_origin[i].items():
            if key == primary_key:
                # primary key found, look in new dictionnary list
                primary_key_value = value
                dl_new_item = {}
                dl_new_item = next((item for item in dl_new if item[primary_key] == primary_key_value), None)
                if dl_new_item == None:
                    # print(primary_key + ' ' + str(primary_key_value) + " not found")
                    event_dict = {}
                    event_dict[primary_key] = primary_key_value
                    event_dict['field_change'] = key
                    event_dict['prev_value'] = primary_key_value
                    event_dict['new_value'] = ''
                    # We want to keep a copy of the object as it is a deleted entry
                    event_dict['event_type'] = event_mapping_rules['deleted_entry']['label']
                    event_dict['object'] = dl_origin[i]                   
                    event_list.append(event_dict)
                    # trigger action based based on event deleted_entry
                    try:
                        trigger_action(event_mapping_rules['deleted_entry']['actions'], dl_origin[i])
                    except:
                        print("oops Action set is not defined for changes on field " +str(key))

    # Iterate through the new dictionnary list to get changes and new entries (we will miss removed entries)
    for i in range(len(dl_new)):
        # Iterate through each key value pairs with the dictionnary (object)
        for key,value in dl_new[i].items():
            if key == primary_key:
                # primary key found, look in original dictionnary list
                primary_key_value = value
                dl_origin_item = {}
                dl_origin_item = next((item for item in dl_origin if item[primary_key] == primary_key_value), None)
                if dl_origin_item == None:
                    # print(primary_key + ' ' + str(primary_key_value) + " not found")
                    event_dict = {}
                    event_dict[primary_key] = primary_key_value
                    event_dict['field_change'] = key
                    event_dict['prev_value'] = ''
                    event_dict['new_value'] = primary_key_value
                    event_dict['event_type']  = event_mapping_rules['new_entry']['label']
                    # We want to keep a copy of the object as it is a new entry
                    event_dict['object'] = dl_new[i]
                    event_list.append(event_dict)   
                    # trigger action based based on event new_entry
                    try:
                        trigger_action(event_mapping_rules['new_entry']['actions'], dl_new[i])
                    except:
                        print("oopdds Action set is not defined for changes on field " +str(key))
                else:
                    dl_origin_item_keys = set(dl_origin_item.keys())
                    dl_new_item_keys = set(dl_new[i].keys()) 
                    intersect_keys = dl_new_item_keys.intersection(dl_origin_item_keys)   
                    modified = {o : (dl_new[i][o], dl_origin_item[o]) for o in intersect_keys if dl_new[i][o] != dl_origin_item[o]}
                    for key,value in modified.items():
                        event_dict = {}
                        event_dict[primary_key] = primary_key_value
                        event_dict['field_change'] = key
                        event_dict['prev_value'] = value[0]
                        event_dict['new_value'] = value[1]
                        if key in event_mapping_rules:
                            event_dict['event_type'] = event_mapping_rules[key]['label'] 
                        else:
                            event_dict['event_type'] = ''
                        event_list.append(event_dict)
                        # trigger action based based on event defined by user
                        try:
                            trigger_action(event_mapping_rules[key]['actions'], dl_new[i])
                        except:
                            print("oops Action set is not defined for changes on field " +str(key))
                break
    print(event_list)

def trigger_action(action_set,data):
    if action_set == 'newjoiner_actions':
        print('generate welcome email to '+data['name'] + ' and exco to assign a buddy')
    elif action_set == 'leaver_actions':
        print('generate email to coo pil to update end date of '+data['name'] )
    elif action_set == 'mobility_actions':
        print('mobility detected')
    else:
        print('no actions are set')

dict_list_compare(dataset_primary_key,dict_list_new,dict_list_old)

new = {
    'igg': 100,
    'rc':'MSC1',
    'location':'Montreal'
}
old = {
    'igg': 100,
    'rc':'J1',
    'location':'New York'
}
added, removed, modified, same = dict_compare(new, old)
events_list = []

for key,value in modified.items():
    event_dict = {}
    event_dict['igg'] = new['igg']
    event_dict['field_change'] = key
    event_dict['prev_value'] = value[0]
    event_dict['new_value'] = value[1]
    events_list.append(event_dict)

# print(events_list)
# event_date,igg,name,field_change,prev_value,new_value
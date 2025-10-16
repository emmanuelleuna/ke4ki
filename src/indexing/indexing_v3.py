from orkg import ORKG, Hosts
from difflib import get_close_matches
import time
import json


# -----------------------------------------
# Connexion au sandbox ORKG
# -----------------------------------------
sandbox_url = "https://sandbox.orkg.org"
orkg = ORKG(host=Hosts.SANDBOX, creds=('emmanuelleuna758@gmail.com', 'Leuna75820u2698@'))
orkg_resources_manager = orkg.resources
orkg_statements_manager = orkg.statements
orkg_litterals_manager = orkg.literals

# -----------------------------------------
# Get template properties
# -----------------------------------------
TEMPLATE_ID = "R677398"
TEMPLATE_PROPERTIES = [
    # Food template --------------------------
    {
        "label": "Food template",
        "propertyShape": "R677462",
        "propertyShapePath": "P142021",
        "propertyShapePathLabel": "food type"
    },
    {
        "label": "Food template",
        "propertyShape": "R677459",
        "propertyShapePath": "P142023",
        "propertyShapePathLabel": "scientific name"
    },
    {
        "label": "Food template",
        "propertyShape": "R677464",
        "propertyShapePath": "P20098",
        "propertyShapePathLabel": "has description"
    },
    {
        "label": "Food template",
        "propertyShape": "R677465",
        "propertyShapePath": "P135009",
        "propertyShapePathLabel": "geographical area"
    },
    {
        "label": "Food template",
        "propertyShape": "R677457",
        "propertyShapePath": "P142020",
        "propertyShapePathLabel": "local name"
    },
    {
        "label": "Food template",
        "propertyShape": "R677461",
        "propertyShapePath": "P142022",
        "propertyShapePathLabel": "food form"
    },
    {
        "label": "Food template",
        "propertyShape": "R677458",
        "propertyShapePath": "P142024",
        "propertyShapePathLabel": "common name"
    },
    {
        "label": "Food template",
        "propertyShape": "R1361187",
        "propertyShapePath": "P142026",
        "propertyShapePathLabel": "food image"
    },
    {
        "label": "Food template",
        "propertyShape": "R707241",
        "propertyShapePath": "P151019",
        "propertyShapePathLabel": "eaten with"
    },
    {
        "label": "Food template",
        "propertyShape": "R707751",
        "propertyShapePath": "P35126",
        "propertyShapePathLabel": "Group"
    },
    {
        "label": "Food template",
        "propertyShape": "R677460",
        "propertyShapePath": "P6003",
        "propertyShapePathLabel": "has ingredient"
    },
    {
        "label": "Food template",
        "propertyShape": "R707240",
        "propertyShapePath": "P62002",
        "propertyShapePathLabel": "food group"
    },
    {
        "label": "Food template",
        "propertyShape": "R677466",
        "propertyShapePath": "P62073",
        "propertyShapePathLabel": "food component"
    },
    
    # Food component template --------------------------
    {
        "label": "Food component template",
        "propertyShape": "R684340",
        "propertyShapePath": ":P62093",
        "propertyShapePathLabel": "food component name"
    },
    {
        "label": "Food component template",
        "propertyShape": "R684342",
        "propertyShapePath": ":P5086",
        "propertyShapePathLabel": "value"
    },
    
    # Quantity Value template --------------------------
    {
        "label": "Quantity Value",
        "propertyShape": "R172467",
        "propertyShapePath": ":P45075",
        "propertyShapePathLabel": "numericValue"
    },
    {
        "label": "Quantity Value",
        "propertyShape": "R172468",
        "propertyShapePath": ":P45076",
        "propertyShapePathLabel": "unit"
    },
]

# -----------------------------------------
# Functions
# -----------------------------------------

# Find or add resource
def find_or_add_resource(label, instanceOf):
    
    r = orkg.resources.get_unpaginated(q=label,exact=True, include=instanceOf)
    r = r.content
   
    if(len(r)>0):
        return r[0]
    else:
        # print(instanceOf)
        r = orkg_resources_manager.add(label=label, classes=instanceOf)
        print('Resource ' + label+ " added")
        return r.content

# Get predicate id from our template
def get_predicate_id(predicate_string):
    predicate_id = None
    for item in TEMPLATE_PROPERTIES:
        if item['propertyShapePathLabel'] == predicate_string:
            predicate_id = item['propertyShapePath']
            return predicate_id

# add statementitem
def add_statement(predicate_string, subject_id, object_classes, extracted_item, object_id=None):
    predicate_found = 0
    if(object_id == None):
        extracted_item = dict(extracted_item)
        label_column = get_close_matches(predicate_string, extracted_item.keys(), n=1, cutoff=cutoff)
        if(len(label_column)>0):
            predicate_found = 1
            label = label_column[0]
            value = extracted_item[label]
            object_resource = find_or_add_resource(label=value, instanceOf=object_classes)
            object_id = object_resource['id']
            
    if(predicate_found == 1):
        
        # -----------------------------------------
        # add {predicate_string} statement
        # -----------------------------------------
        # get statements by subject and predicate without paggination
        statements_subject_predicate = orkg_statements_manager.get_by_subject_and_predicate_unpaginated(subject_id, get_predicate_id(predicate_string))
        statements_subject_predicate = statements_subject_predicate.content
        # get statements by predicate and object without paggination
        statements_object_predicate = orkg_statements_manager.get_by_object_and_predicate_unpaginated(object_id, get_predicate_id(predicate_string))
        statements_object_predicate = statements_object_predicate.content
        # check if statement already exist
        if(statements_subject_predicate.__len__() == 0 | statements_object_predicate.__len__() == 0):
            print('The statement '+subject_id+' '+predicate_string+' '+object_id +' does not exist')
            print('Adding of the statement ...')
            # add statement
            orkg_statements_manager.add(subject_id=subject_id, predicate_id=get_predicate_id(predicate_string), object_id=object_id)
        else:
            # Obtenir les IDs de chaque liste
            ids_liste2 = {item["id"] for item in statements_object_predicate}

            # Intersection : éléments de liste1 dont l'id est dans liste2
            intersection = [item for item in statements_subject_predicate if item["id"] in ids_liste2]
            if(intersection.__len__() == 0):
                print('The statement '+subject_id+' '+predicate_string+' '+object_id +' does not exist')
                print('Adding of the statement ...')
                # add statement
                orkg_statements_manager.add(subject_id=subject_id, predicate_id=get_predicate_id(predicate_string), object_id=object_id)
            else: 
                print('The statement '+subject_id+' '+predicate_string+' '+object_id +' already exist')
                print('skipping of the statement ...')


# -----------------------------------------
# Get extracted data
# -----------------------------------------
# Exemple: chargement depuis un fichier JSONL ou JSON
file_path = "run_parsed/parsed_prediction_run6.json"  # ou "predictions.json"
all_pred = []

# Détection automatique du format (JSONL ou JSON classique)
if file_path.endswith(".jsonl"):
    with open(file_path, "r", encoding="utf-8") as f:
        all_pred = [json.loads(line) for line in f]
else:
    with open(file_path, "r", encoding="utf-8") as f:
        all_pred = json.load(f)
    

# Fusionner toutes les prédictions en une seule liste
merged_predictions = []

for item in all_pred:
    predictions = item.get("prediction", [])
    predictions = json.loads(predictions)
    # Ajoute chaque prédiction à la liste globale
    for p in predictions:
        merged_predictions.append(p)

data = merged_predictions

# data = [
#   {
#     "geographical area": "West african",
#     "local name": "Salt",
#     "common name": "Salt",
#     "food group": "Miscellaneous",
#     "food components": [
#       { "label": "Salt01_Energy", "value": 0.0, "unit": "Kcal" },
#       { "label": "Salt01_Water", "value": 0.5, "unit": "g" },
#       { "label": "Salt01_Protein", "value": 0.0, "unit": "g" },
#       { "label": "Salt01_Fat", "value": 0.0, "unit": "g" },
#       { "label": "Salt01_Carbohydrate", "value": 0.0, "unit": "g" },
#       { "label": "Salt01_Fibre", "value": 0.0, "unit": "g" },
#       { "label": "Salt01_Ash", "value": 99.8, "unit": "g" },
#       { "label": "Salt01_Calcium", "value": 216.0, "unit": "mg" },
#       { "label": "Salt01_Fer", "value": 1.2, "unit": "mg" },
#       { "label": "Salt01_Magnesium", "value": 39.0, "unit": "mg" },
#       { "label": "Salt01_Phosphore", "value": 166.0, "unit": "mg" },
#       { "label": "Salt01_Potassium", "value": 1290.0, "unit": "mg" },
#       { "label": "Salt01_Sodium", "value": 38760.0, "unit": "mg" },
#       { "label": "Salt01_Zinc", "value": 0.1, "unit": "mg" }
#     ]
#   }
# ]

# Start the timer
start = time.time()

# -----------------------------------------
# Map extracted data
# -----------------------------------------
mapped_data = []
cutoff = 0.90
for item in data:
    properties_found = []
    for property in TEMPLATE_PROPERTIES:
        label_found = get_close_matches(property["propertyShapePathLabel"], item.keys(), n=1, cutoff=cutoff)
        
        if(len(label_found) >0):
            properties_found.append(label_found[0])
            
    # get value in item for each property foud
    item_properties = {}
    for prop in properties_found:
        item_properties[prop] = item[prop]
    
    # add mapped item to mapped_data
    mapped_data.append(item_properties)
    
# -----------------------------------------
# Calculate (completeness) of field and number of indexable item
# -----------------------------------------
def est_non_vide(val):
    return val is not None and val != ""

def is_indexable(item):
    return "local name" in item.keys()

def calculate_indexable_item(liste):
    return sum(1 for item in liste if is_indexable(item))/len(liste)

def completude_element(ref, test):
    champs_attendus = [k for k, v in ref.items() if est_non_vide(v)]
    if not champs_attendus:
        return 100.0  # si rien à tester, on considère 100%
    champs_complets = [k for k in champs_attendus if k in test and est_non_vide(test[k])]
    return len(champs_complets) / len(champs_attendus) * 100

def completude_liste(liste1, liste2):
    completudes = []
    for ref, test in zip(liste1, liste2):
        score = completude_element(ref, test)
        completudes.append(score)
    moyenne = sum(completudes) / len(completudes)
    return completudes, moyenne

completudes, moyenne = completude_liste(data, mapped_data)
indexing_rate = calculate_indexable_item(mapped_data)
print("Completeness by element :", completudes)
print("Total completeness :", moyenne)
print('indexing rate: ', indexing_rate)
print('Number of items: ', len(mapped_data))

# -----------------------------------------
# Adding the contribution
# -----------------------------------------

# test -------------------------------------------------------------------------------
# test = orkg.statements.add(subject_id='R1', predicate_id='P2', object_id='L3')
# print(test.content)
# print("Test Ok")
# test -------------------------------------------------------------------------------

# Stop the timer

indexed_statement = []
resources_urls = []
for item in mapped_data:
    # -----------------------------------------
    # Create or get the general ressource (Food)
    # -----------------------------------------
    nb_statement = 0
    item = dict(item)
    label_column = get_close_matches("local name", item.keys(), n=1, cutoff=cutoff)
    if(label_column.__len__() > 0):
        label = label_column[0]
        value = item[label]
        general_resource = find_or_add_resource(label=value, instanceOf=['C34019'])
        resource_url = f"https://sandbox.orkg.org/resources/{general_resource['id']}?noRedirect"
        
        # -----------------------------------------
        # add local name statement
        # -----------------------------------------
        # Here the object is also the subject
        add_statement(predicate_string="local name", subject_id=general_resource['id'], object_classes=['C34019'], extracted_item=item)
        nb_statement += 1
        
        # -----------------------------------------
        # add scientific name statement
        # -----------------------------------------
        if( get_close_matches("local name", item.keys(), n=1, cutoff=cutoff).__len__() >0):
            add_statement("scientific name", general_resource['id'], ['C86010'], item)
            nb_statement += 1
        
        # -----------------------------------------
        # add common name statement
        # -----------------------------------------
        if(get_close_matches("common name", item.keys(), n=1, cutoff=cutoff).__len__() >0):
            add_statement("common name", general_resource['id'], ['C34019'], item)
            nb_statement += 1
        
        # -----------------------------------------
        # add food group statement
        # -----------------------------------------
        if(get_close_matches("food group", item.keys(), n=1, cutoff=cutoff).__len__() >0):
            add_statement("food group", general_resource['id'], ['C34000'], item)
            nb_statement += 1
        
        # -----------------------------------------
        # add geographical area statement
        # -----------------------------------------
        if(get_close_matches("geographical area", item.keys(), n=1, cutoff=cutoff).__len__() >0):
            add_statement("geographical area", general_resource['id'], ['C86012'], item)
            nb_statement += 1
        
        # -----------------------------------------
        # add food form statement
        # -----------------------------------------
        if(get_close_matches("food form", item.keys(), n=1, cutoff=cutoff).__len__() >0):
            add_statement("food form", general_resource['id'], ['C86013'], item)
            nb_statement += 1
        
        # -----------------------------------------
        # add food components statement
        # -----------------------------------------
        if(get_close_matches("food components", item.keys(), n=1, cutoff=cutoff).__len__() >0):
            for component in item['food components']:
                component = dict(component)
                c = find_or_add_resource(label=item['local name']+'_'+ component['label'],instanceOf=["C34009"])                
                # add food component name statement
                
                if( "label" in component.keys()):
                    add_statement("food component name", c['id'], ['C34009'], {
                        "food component name": component["label"]
                    })
                    
                # add food component value statement C23008
                if( "value" in component.keys() and "unit" in component.keys()):
                    v = find_or_add_resource(label=str(component['value'])+' '+ str(component['unit']),instanceOf=["C23008"])

                    # add numericValue value statement
                    l = orkg_litterals_manager.get_all(q=component["value"], exact=True)
                    l = l.content
                    if(len(l)==0 ):
                        l = orkg_litterals_manager.add(label=component["value"], datatype='xsd:decimal')
                        l = l.content
                    else:
                        l = l[0]
                    add_statement("numericValue", v['id'], ['literal'], None, l['id'])

                    # add unit value statement
                    add_statement("unit", v['id'], ['C23009'], component)
                    
                    add_statement("value", c['id'], ['C23008'], None, v['id'])
                    
                    
                add_statement("food components", general_resource["id"], ['C34009'], None, c["id"])
                nb_statement += 1
        
        # -----------------------------------------
        # add food ingredient statement
        # -----------------------------------------
        if( "ingredients" in item.keys()):
            for ingredient in item['ingredients']:
                ingredient = dict(ingredient)
                i = find_or_add_resource(label=item['local name']+'_ingredient'+ ingredient['label'], instanceOf="C77007")
                
                # add food ingredient common name statement
                if( "common name" in ingredient.keys()):
                    add_statement("common name", i['id'], ['C34019'], ingredient)
                    
                # add food ingredient scientific name statement
                if( "scientific name" in ingredient.keys()):
                    add_statement("scientific name", i['id'], ['C86010'], ingredient)
                    
                add_statement("has ingredient", general_resource["id"], ['C77007'], None, i["id"])
                nb_statement += 1
                
        # get the resource statements
        general_ressources_statements = orkg_statements_manager.get_by_subject_unpaginated(general_resource['id'])
        general_ressources_statements = general_ressources_statements.content
        indexed_statement.append(general_ressources_statements)
        
        # print statement list
        print(f"\n\nnumber of statements:  {general_ressources_statements.__len__()}")
        
        # adding resource url
        resources_urls.append({
            "label":value,
            "url": resource_url
        })
    else:
        print('This ressource can not be index')


json.dump(resources_urls, open('resources_urls_run6.json', 'w'), indent=4)
# -----------------------------------------
# 
# -----------------------------------------

# Stop the timer
end = time.time()
print(f"Execution time : {end - start:.4f} seconds")
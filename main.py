import csv
import re

csv_file_path = './mch.csv'
csv_file_path_2 = './mch_nonfood105.csv'
txt_file_path = 'output.txt'
txt_file_path_1 = 'output_produce.txt'
txt_file_path_2 = 'output_GNF105.txt'
txt_file_path_3 = 'output_GL101.txt'
txt_file_path_4 = 'output_GD106.txt'
txt_file_path_5 = 'output_BCK&HD.txt'
txt_file_path_6 = 'output_GF103&GF104.txt'
txt_file_path_7 = 'output_meat&seafood.txt'


# 存储所有的query
# 2个字典分别存储父类目名称和税率
# 目前后台一级类目被分成6个
listQ = []

# 更新的顺序如下
# Produce
# Grocery Non Food (105)
# Grocery Leisure (101)
# Grocery Dry (106)
# HOT DELI
# Grocery Frozen / Grocery Deli (103,104)
# Meat / Seafood
# 为了方便区分，另外9个list分别存取不同类目
listQ_1 = []
listQ_2 = []
listQ_3 = []
listQ_4 = []
listQ_5 = []
listQ_6 = []
listQ_7 = []

listQ_11 = []
listQ_21 = []
listQ_31 = []
listQ_41 = []
listQ_51 = []
listQ_61 = []
listQ_71 = []

# 统计有多少重复的path
old_set = {
    'Frozen > Meat Ball',
'Frozen > Meat Ball > Paste',
'Deli > Bun (Plain)',
'Deli > Cake',
'Deli > Cake > Pancake',
'Grocery > Nut',
'Grocery > Nut > MixNut',
'Grocery > Nut > MixNut > Peanut',
'Grocery > Chocolate',
'Grocery > Chocolate > Choc. Bar',
'Grocery > Can',
'Grocery > Can > Seasoning Meat',
'Grocery > Rice Cracker',
'Grocery > Rice Cracker > Popcorn',
'Grocery > Cooking Wine',
'Frozen > Frozen Noodle',
'Grocery > Noodle',
'Grocery > Noodle > Wheat Noodle',
'Grocery > Rice Seasoning',
'Grocery > Can Soup',
'Grocery > Can Soup > Soup Base',
'Deli > Fish Cake',
'Deli > Fish Cake > Crab Meat',
'Grocery > Short Grain',
'Frozen > Frz Instant Noodle',
'Grocery > Brown Rice',
'Grocery > Premix Flour',
'Grocery > Premix Flour > Batter',
'Deli > Pickled Vegetable',
'Grocery > Canned Vegetable',
'Frozen > Frz Dim Sum',
'Frozen > Frz Dim Sum > Egg Roll',
'Frozen > Frozen Meat',
'Grocery > Candy',
'Grocery > Candy > Gum',
'Grocery > Canned',
'Grocery > Canned > Jar Dessert',
'Grocery > Salt',
'Grocery > Salt > Sugar',
'Grocery > Wheat Flour-All type',
'Grocery > Canned > Jar Fruit',
'Grocery > Coconut Milk',
'Grocery > Coconut Milk > Powder',
'Frozen > Frz  Dessert',
'Frozen > Frz  Dessert > Cake',
'Grocery > Honey',
'Grocery > Honey > Jam',
'Grocery > Honey > Jam > PnutButter',
'Grocery > Tea',
'Grocery > Tea > Milk Tea',
'Grocery > Tea > Milk Tea > Tea Bag',
'Deli > Salted Meat',
'Deli > Salted Meat > Sausage',
'Grocery > Package Meal',
'Grocery > Package Meal > Conge',
'Deli > Rice cake',
'Deli > Cheese',
'Grocery > Moon cake',
'Frozen > Seafood ball',
'Frozen > Seafood ball > Paste',
'Frozen > Frz Rice Ball',
'Grocery > Condensed',
'Grocery > Condensed > Evapo.Milk',
'Deli > Wheat',
'Deli > Wheat > Egg Noodle',
'Taxable Grocery > Cooker',
'Taxable Grocery > Cooker > Rice Cooker',
'Grocery > Instant Marinade Mix',
'Grocery > Seasoning Sauce',
'Grocery > Bean Thread',
'Frozen > Frz Pancake',
'Frozen > Frz Pancake > Waffle',
'Deli > Juice',
'Deli > Juice > Punch',
'Deli > Soymilk',
'Grocery > Tea > Coffee Drink',
'Deli > Butter',
'Deli > Butter > Margarine',
'Deli > Tofu Deli',
'Grocery > Soy Sauce',
'Grocery > Chips',
'Grocery > Chips > Shrimp Chips',
'Grocery > Hot Cereal',
'Grocery > Hot Cereal > Oatmeal',
'Frozen > Frz Dumpling',
'Grocery > Instant Noodle',
'Taxable Grocery > Cleaner',
'Grocery > Salad Dressing',
'Taxable Grocery > Hair Care',
'Deli > Meat Ball',
'Deli > Meat Ball > Meat Paste',
'Deli > Wrapper',
'Deli > Wrapper > Wonton Skin',
'Taxable Grocery > Wellness',
'Deli > Yogurt',
'Deli > Yogurt > Yogurt drink',
'Deli > Dried',
'Deli > Dried > Salted Seafood',
'Grocery > Cookies',
'Grocery > Mix Drink Powder',
'Taxable Grocery > Dental Care',
'Grocery > Ginseng',
'Seafood > Squid Frozen',
'Seafood > Cooked Shrimp Frozen',
'Seafood > Cuttlefish',
'Seafood > Shellfish Frozen',
'Seafood > Whole Fish Frozen',
'Seafood > Scallop Frozen',
'Grocery > Cooking Oil',
'Frozen > Frz Fruit',
'Frozen > Frz Fruit > Vegetable',
'Grocery > BBQ Sauce',
'Grocery > Vinegar',
'Grocery > Soy.MIlk.Rice Drink',
'Taxable Grocery > Gas',
'Taxable Grocery > Gas > Charcoal',
'Taxable Grocery > Gas > Charcoal > Grill',
'Deli > Sausage',
'Deli > Sausage > Hot Dog',
'Deli > Sausage > Hot Dog > Ham',
'Grocery > Chili Sauce',
'Grocery > Chili Sauce > Sweet',
'Grocery > Curry Powder',
'Grocery > Curry Powder > Curry',
'Grocery > Pastry',
'Grocery > Pastry > Cake',
'Grocery > Pastry > Cake > Cookie',
'Taxable Grocery > Glassware',
'Grocery > Dried Bean',
'Grocery > Dried Bean > Nut',
'Grocery > Dried Bean > Nut > Seed',
'Deli > Sweet Dessert',
'Deli > Sweet Dessert > Cake',
'Deli > Bun (w/Filling)',
'Meat > Quail',
'Taxable Grocery > Vitamin',
'Taxable Grocery > Vitamin > Supplement',
'Vegetables > Mushroom',
'Deli > Liq.Cream',
'Deli > Liq.Cream > coffeemate',
'Grocery > Steak Sauce',
'Grocery > Steak Sauce > DipSauce',
'Grocery > Rice Flour',
'Grocery > Seasoning',
'Grocery > Seasoning > MSG',
'Grocery > Seasoning > MSG > Spice',
'Deli > Milk',
'Frozen > Ice Cream',
'Frozen > Ice Cream > Popsicle',
'Frozen > Frz Instant Meal',
'Grocery > Canned > Jar Gluten',
'Frozen > Frz Bun (salty)',
'Frozen > Frz Wrapper',
'Frozen > Frz Instant Rice',
'Deli > Miso',
'Grocery > Instant Soup Mix',
'Grocery > Dried Seafood',
'Grocery > Soda',
'Grocery > Soda > CarbonateDrink',
'Deli > Yam Cake Konnyaku',
'Deli > Udon',
'Grocery > Sweet Rice',
'Grocery > Wasabi',
'Grocery > Wasabi > Mustard',
'Grocery > Mayonnaise',
'Grocery > Yogurt Drink',
'Grocery > Assort. Gift Pack',
'Grocery > Seafood Sauce',
'Grocery > Seafood Sauce > Paste',
'Grocery > Bean Paste',
'Grocery > Juice (50% or less)',
'Grocery > Pres.',
'Grocery > Pres. > Marinate Snack',
'Deli > Bean cake',
'Deli > Bean cake > Gluten',
'Grocery > Dried Vegetable',
'Grocery > Dried Vegetable > Herb',
'Vegetables > Leaf Vegetable',
'Deli > Vegetarian food',
'Vegetables > Root',
'Grocery > Juice',
'Grocery > Juice > Cocktail Mix',
'Fruits > Melons',
'Vegetables > Botanical Fruit',
'Vegetables > Bulb',
'Vegetables > Seed',
'Vegetables > Seed > Sprout',
'Fruits > Apple',
'Vegetables > Stem',
'Vegetables > Stem > Tuber Vegetable',
'Meat > Pork',
'Meat > Pork > Pig',
'Meat > Beef',
'Meat > Beef > Ox',
'Meat > Goat',
'Meat > Goat > Lamb',
'Meat > Chicken',
'Fruits > Stone Fruits',
'Meat > Duck',
'Seafood > Whole Fish',
'Fruits > Bananas',
'Seafood > Fish Ball Frozen',
'Seafood > Fish Steak Frozen',
'Fruits > Pears',
'Fruits > Tropical Fruit',
'Fruits > Grapes',
'Bakery > OPEN CASE',
'Bakery > OPEN CASE > B',
'Bakery > Roll Cake',
'Vegetables > Nut',
'Taxable Grocery > Facial Care',
'Grocery > Marinate',
'Grocery > Marinate > Pickled Veg',
'Grocery > Seafood Snack',
'Grocery > Coffee',
'Grocery > Coffee > Cocoa',
'Grocery > Coffee > Cocoa > Choco',
'Grocery > Herb Tea (Can& Botl)',
'Frozen > Frz Bun (Sweet)',
'Frozen > Frz Bun-Plain',
'Frozen > Frz Bun-Plain > Dough',
'Grocery > Canned > Jar Seafood',
'Grocery > Jelly',
'Grocery > Jelly > Pudding',
'Grocery > Jelly > Pudding > Mochi',
'Taxable Grocery > Paper Goods',
'Grocery > Preserved Bean Curd',
'Taxable Grocery > Cookware',
'Taxable Grocery > Cookware > Pot',
'Taxable Grocery > Cookware > Pot > Pan',
'Grocery > Syrup',
'Frozen > Frz Vegetarian Food',
'Grocery > Dried Seaweed',
'Grocery > Dried Seaweed > Nori',
'Taxable Grocery > Bamboo',
'Taxable Grocery > Bamboo > Chopsticks',
'Taxable Grocery > Accessories',
'Taxable Grocery > Accessories > Utensil',
'Taxable Grocery > Body wear',
'Taxable Grocery > Body wear > Gloves',
'Frozen > FRZ MOON CAKE',
'Taxable Grocery > Soap',
'Taxable Grocery > Soap > Liquid Soap',
'Taxable Grocery > Body Care',
'Taxable Grocery > Body Care > Lotion',
'Taxable Grocery > Vacuum Flash',
'Taxable Grocery > Vacuum Flash > Tea Pot',
'Taxable Grocery > Boiler',
'Grocery > Energy',
'Grocery > Energy > Sport Drink',
'Deli > Duck',
'Deli > Duck > Quail',
'Deli > Duck > Quail > Balut Egg',
'Deli > Rice Noodle',
'Deli > Rice Noodle > RiceRoll',
'Seafood > Mixed Seafood Frozen',
'Frozen > Frz Rice Cake&Noodle',
'Deli > Preserved Egg',
'Grocery > Fish Sauce',
'Grocery > Long Grain',
'Grocery > RiceNoodle',
'Grocery > RiceNoodle > RiceStick',
'Grocery > Corn Starch',
'Grocery > Corn Starch > Starch',
'Deli > Salted Egg',
'Grocery > Canned Gelatin',
'Grocery > Seasoned Bean Curd',
'Grocery > Flavor Seed',
'Grocery > ConcentrateJuice',
'Grocery > ConcentrateJuice > Vin',
'Taxable Grocery > Chinaware',
'Taxable Grocery > Chinaware > Casserole',
'Taxable Grocery > Cleaning Needs',
'Taxable Grocery > Melanie',
'Taxable Grocery > Japanese Porcelain',
'Taxable Grocery > Mixer',
'Taxable Grocery > Mixer > Extractor',
'Grocery > Pres. Dry  Fruit',
'Grocery > Baby Food',
'Grocery > Gelatin',
'Grocery > Gelatin > Agar Mix',
'Deli > Gelatin',
'Deli > Gelatin > Pudding',
'Deli > Seafood ball',
'Deli > Seafood ball > Paste',
'Grocery > Sesame Oil',
'Grocery > Sesame Oil > Chili Oil',
'Grocery > Tapioca Pearl',
'Grocery > Tapioca Pearl > Boba',
'Grocery > Rice Paper',
'Seafood > Fish Fillet Frozen',
'Bakery > Cheese Cake',
'Frozen > Popsicle-Juice<=50%',
'Seafood > Marinated',
'Seafood > Marinated > SmokedFish',
'Deli > Bean Sauce',
'Seafood > Sashimi',
'Taxable Grocery > Stove',
'Taxable Grocery > Stove > Frying Pot',
'Grocery > Cereal',
'Taxable Grocery > ExternalUse Medicine',
'Grocery > Jerky',
'Deli > White',
'Deli > White > Brown Egg',
'Taxable Grocery > Daiper',
'Taxable Grocery > Decoration',
'Bakery > OPEN CASE > A',
'Flower > Plants',
'Bakery > Room Temp. Cake OEM',
'Frozen > Frz Juice(>50%Juice)',
'Grocery > Starch Sht',
'Grocery > Starch Sht > Chip unck',
'Grocery > Pasta',
'Grocery > Pasta > Macaroni',
'Grocery > Bread',
'Taxable Grocery > Mop',
'Taxable Grocery > Mop > Broom',
'Fruits > Citrus',
'Deli > Ready to Eat Meal',
'Taxable Grocery > Plastic Houseware',
'Taxable Grocery > Plastic Kitchen Ware',
'Grocery > Baking Powder',
'Grocery > Baking Powder > Yeast',
'Meat > Squab',
'Bakery > Toast',
'Vegetables > Flower Vegetable',
'Grocery > Pre Cooked Rice',
'Grocery > Water',
'Grocery > Ketchup',
'Grocery > Ketchup > Tomato Sauce',
'Seafood > Shellfish',
'Fruits > Berries',
'Seafood > Shrimp',
'Grocery > Dietary Supplement',
'Seafood > Shrimp Frozen',
'Bakery > ROOM TEMP. CAKE',
'Deli > Deli Coffee',
'Grocery > Bulk-Dried Vegetable',
'Taxable Grocery > Detergents',
'Taxable Grocery > Detergents > Softener',
'Seafood > Seafood Cucumber Frz',
'Seafood > Fish Ball',
'Frozen > Frozen Seafood',
'Grocery > Canned > Jar Beans',
'Bakery > Western Dessert',
'Seafood > Frog Leg Frozen',
'Grocery > Mixed Grain',
'Bakery > BF Small Bread',
'Seafood > Imitation Crab meat',
'Meat > Partridge',
'Seafood > Lobster',
'Seafood > Octopus Frozen',
'Seafood > Crab Frozen',
'Taxable Grocery > Pesticide',
'Frozen > Frozen Yogurt',
'Bakery > Croissant',
'Bakery > Croissant > Danish',
'Seafood > Crab',
'Vegetables > Salad',
'Vegetables > Salad > Veg. Sliced',
'Seafood > Roe Frozen',
'Bakery > BF Toast',
'Bakery > BF Toast > Loaf Bread',
'Bakery > Roll',
'Grocery > Pasta Sauce',
'Grocery > Preserved Salted Veg',
'Hot Deli > STEAMED BUN',
'Vegetables > Herb Vegetable',
'Hot Deli > Bento-Comb Meal',
'Hot Deli > JAPANESE ENTREE',
'Taxable Grocery > Menstrual Hygiene',
'Hot Deli > USDA Marin Cook Prod',
'Taxable Grocery > Baby Needs',
'Hot Deli > FDA Rdy to Eat Prod',
'Hot Deli > FDA Dim Sum & Buns',
'Hot Deli > USDA BBQ Prod',
'Hot Deli > COLD DELI RAW',
'Hot Deli > USDA Steamed Bun',
'Seafood > Fish Steak',
'Frozen > FrzJuice <50%juice',
'Seafood > Cuttlefish Frozen',
'Hot Deli > DUMPLING',
'Seafood > Dried',
'Seafood > Dried > Cooked',
'Seafood > Dried > Cooked > Steamed',
'Grocery > Non Alocoholic Beer',
'Taxable Grocery > Fan',
'Taxable Grocery > Fan > Cooler Fan',
'Taxable Grocery > Fan > Cooler Fan > AC',
'Meat > Turkey',
'Hot Deli > COLD DELI WTH MEAT',
'Hot Deli > COLD DELI MARINATED',
'Hot Deli > COLD DELI VEGETARIAN',
'Seafood > Paste',
'Taxable Grocery > Oven',
'Taxable Grocery > Oven > Microwave Oven',
'Hot Deli > BBQ PORK',
'Taxable Grocery > Air Freshener',
'Hot Deli > Cooking Sauce',
'Taxable Grocery > Makeup',
'Meat > Rabbit',
'Grocery > Wheat Grain',
'Meat > Geese',
'Hot Deli > BBQ POULTRY',
'Taxable Grocery > Electronic',
'Taxable Grocery > Joss Material',
'Taxable Grocery > Joss Material > Candle',
'Taxable Grocery > Stuffed Animals',
'Taxable Grocery > Stuffed Animals > Toy',
'Hot Deli > Bake Service',
'Hot Deli > HK Dim Sum',
'Bakery > BF Croissant',
'Bakery > BF Croissant > Danish',
'Hot Deli > C',
'Hot Deli > C > D ASIAN DIMSUM',
'Hot Deli > RM LOCAL COLD',
'Hot Deli > RM LOCAL COLD > WET',
'Hot Deli > FDA Seafood Product',
'Taxable Grocery > Stationary',
'Bakery > Cookies & Tart',
'Bakery > Chinese Dessert',
'Bakery > ROOM TEMP. DESSET',
'Hot Deli > Sushi',
'Hot Deli > USDA Dim Sum Product',
'Seafood > Fried Fish',
'Hot Deli > CHINESE DIM SUM',
'Hot Deli > BBQ SAUCE',
'Grocery > Bulk-Pres',
'Grocery > Bulk-Pres > Dry Fruit',
'Hot Deli > USDA Marin Prod',
'Grocery > Non Alocoholic Wine',
'Grocery > Discontinued Article',
'Grocery > Non-Alcoholic Beer',
'Grocery > Red Wine Other',
'Seafood > Fish Fillet',
'Meat > Deer',
'Taxable Grocery > Battery',
'Grocery > Rolls',
'Frozen > Ice',
'Taxable Grocery > Dog food',
'Grocery > Pet Toy',
'Taxable Grocery > Cat food',
'Hot Deli > Bento',
'Produce > Stem > Tuber Vegetable',
'Produce > Seed > Sprout',
'Produce > Grains > Legumes',
'Seafood > Frozen Shellfish',
}
GL101_set = {
    'Grocery > Moon cake',
    'Frozen > FRZ MOON CAKE',
    'Grocery > Condensed',
    'Grocery > Condensed > Evapo.Milk',
    'Grocery > Coffee',
    'Grocery > Coffee > Cocoa',
    'Grocery > Coffee > Cocoa > Choco',
    'Deli > Deli Coffee',
    'Grocery > Tea',
    'Grocery > Tea > Milk Tea',
    'Grocery > Tea > Milk Tea > Tea Bag',
    'Grocery > Tea > Coffee Drink',
    'Grocery > Mix Drink Powder',
    'Grocery > Herb Tea (Can& Botl)',
    'Grocery > Soda',
    'Grocery > Soda > CarbonateDrink',
    'Grocery > Energy',
    'Grocery > Energy > Sport Drink',
    'Deli > Juice',
    'Deli > Juice > Punch',
    'Grocery > Juice',
    'Grocery > Juice > Cocktail Mix',
    'Grocery > ConcentrateJuice',
    'Grocery > ConcentrateJuice > Vin',
    'Grocery > Water',
    'Frozen > FrzJuice <50%juice',
    'Deli > Yogurt',
    'Deli > Yogurt > Yogurt drink',
    'Grocery > Soy.MIlk.Rice Drink',
    'Grocery > Yogurt Drink',
    'Grocery > Dietary Supplement',
    'Grocery > Chocolate',
    'Grocery > Chocolate > Choc. Bar',
    'Grocery > Candy',
    'Grocery > Candy > Gum',
    'Grocery > Rice Cracker',
    'Grocery > Rice Cracker > Popcorn',
    'Grocery > Cookies',
    'Grocery > Assort. Gift Pack',
    'Grocery > Nut',
    'Grocery > Nut > MixNut',
    'Grocery > Nut > MixNut > Peanut',
    'Grocery > Flavor Seed',
    'Grocery > Chips',
    'Grocery > Chips > Shrimp Chips',
    'Grocery > Jelly',
    'Grocery > Jelly > Pudding',
    'Grocery > Jelly > Pudding > Mochi',
    'Grocery > Seafood Snack',
    'Grocery > Seasoned Bean Curd',
    'Grocery > Jerky',
    'Grocery > Pres.',
    'Grocery > Pres. > Marinate Snack',
    'Grocery > Pres. Dry  Fruit',
    'Grocery > Pastry',
    'Grocery > Pastry > Cake',
    'Grocery > Pastry > Cake > Cookie',
    'Grocery > Hot Cereal',
    'Grocery > Hot Cereal > Oatmeal',
    'Grocery > Cereal'
}
GD106_set = {
    'Grocery > Gelatin > Agar Mix',
'Grocery > Baking Powder',
'Grocery > Premix Flour > Batter',
'Grocery > BBQ Sauce',
'Grocery > Bean Paste',
'Grocery > Bean Thread',
'Grocery > Tapioca Pearl > Boba',
'Grocery > Brown Rice',
'Grocery > Can',
'Grocery > Can Soup',
'Grocery > Canned',
'Grocery > Canned Gelatin',
'Grocery > Canned Vegetable',
'Grocery > Sesame Oil > Chili Oil',
'Grocery > Chili Sauce',
'Grocery > Coconut Milk',
'Grocery > Package Meal > Conge',
'Grocery > Cooking Oil',
'Grocery > Cooking Wine',
'Grocery > Corn Starch',
'Grocery > Curry Powder > Curry',
'Grocery > Curry Powder',
'Grocery > Dietary Supplement',
'Grocery > Steak Sauce > DipSauce',
'Grocery > Dried Bean',
'Grocery > Dried Seaweed',
'Grocery > Dried Vegetable',
'Grocery > Fish Sauce',
'Grocery > Gelatin',
'Grocery > Ginseng',
'Grocery > Dried Vegetable > Herb',
'Grocery > Honey',
'Grocery > Instant Marinade Mix',
'Grocery > Instant Noodle',
'Grocery > Instant Soup Mix',
'Grocery > Honey > Jam',
'Grocery > Canned > Jar Dessert',
'Grocery > Canned > Jar Fruit',
'Grocery > Canned > Jar Gluten',
'Grocery > Canned > Jar Seafood',
'Grocery > Ketchup',
'Grocery > Long Grain',
'Grocery > Marinate',
'Grocery > Mayonnaise',
'Grocery > Mixed Grain',
'Grocery > Seasoning > MSG',
'Grocery > Wasabi > Mustard',
'Grocery > Noodle',
'Grocery > Dried Seaweed > Nori',
'Grocery > Dried Bean > Nut',
'Grocery > Package Meal',
'Grocery > Seafood Sauce > Paste',
'Grocery > Marinate > Pickled Veg',
'Grocery > Honey > Jam > PnutButter',
'Grocery > Coconut Milk > Powder',
'Grocery > Pre Cooked Rice',
'Grocery > Premix Flour',
'Grocery > Preserved Bean Curd',
'Grocery > Preserved Salted Veg',
'Grocery > Rice Flour',
'Grocery > Rice Paper',
'Grocery > Rice Seasoning',
'Grocery > RiceNoodle',
'Grocery > RiceNoodle > RiceStick',
'Grocery > Salad Dressing',
'Grocery > Salt',
'Grocery > Seafood Sauce',
'Grocery > Seasoning',
'Grocery > Can > Seasoning Meat',
'Grocery > Seasoning Sauce',
'Grocery > Dried Bean > Nut > Seed',
'Grocery > Sesame Oil',
'Grocery > Short Grain',
'Grocery > Can Soup > Soup Base',
'Grocery > Soy Sauce',
'Grocery > Seasoning > MSG > Spice',
'Grocery > Corn Starch > Starch',
'Grocery > Steak Sauce',
'Grocery > Salt > Sugar',
'Grocery > Chili Sauce > Sweet',
'Grocery > Sweet Rice',
'Grocery > Syrup',
'Grocery > Tapioca Pearl',
'Grocery > Ketchup > Tomato Sauce',
'Grocery > Vinegar',
'Grocery > Wasabi',
'Grocery > Wheat Flour-All type',
'Grocery > Wheat Grain',
'Grocery > Noodle > Wheat Noodle',
'Grocery > Baking Powder > Yeast'
}
BCKHD_set = {
    'Bakery > OPEN CASE > A',
'Hot Deli > Bake Service',
'Hot Deli > BBQ PORK',
'Hot Deli > BBQ POULTRY',
'Hot Deli > Bento-Comb Meal',
'Bakery > BF Small Bread',
'Bakery > BF Toast',
'Bakery > Cheese Cake',
'Hot Deli > COLD DELI MARINATED',
'Hot Deli > COLD DELI RAW',
'Hot Deli > COLD DELI VEGETARIAN',
'Hot Deli > COLD DELI WTH MEAT',
'Hot Deli > Cooking Sauce',
'Bakery > Croissant',
'Bakery > Croissant > Danish',
'Hot Deli > DUMPLING',
'Hot Deli > C > D ASIAN DIMSUM',
'Hot Deli > FDA Dim Sum & Buns',
'Hot Deli > FDA Rdy to Eat Prod',
'Hot Deli > FDA Seafood Product',
'Hot Deli > HK Dim Sum',
'Hot Deli > JAPANESE ENTREE',
'Bakery > BF Toast > Loaf Bread',
'Hot Deli > RM LOCAL COLD',
'Bakery > Roll',
'Bakery > Roll Cake',
'Bakery > ROOM TEMP. CAKE',
'Bakery > Room Temp. Cake OEM',
'Hot Deli > STEAMED BUN',
'Hot Deli > Sushi',
'Bakery > Toast',
'Hot Deli > USDA BBQ Prod',
'Hot Deli > USDA Marin Cook Prod',
'Hot Deli > USDA Steamed Bun',
'Bakery > Western Dessert',
'Hot Deli > RM LOCAL COLD > WET'
}
GF103_set = {
    'Deli > Duck > Quail > Balut Egg',
'Grocery > BBQ Sauce',
'Deli > Bean cake',
'Grocery > Bean Paste',
'Deli > White > Brown Egg',
'Deli > Bun (Plain)',
'Deli > Bun (w/Filling)',
'Deli > Butter',
'Deli > Sweet Dessert > Cake',
'Frozen > Frz  Dessert > Cake',
'Deli > Cake',
'Deli > Cheese',
'Grocery > Chili Sauce',
'Grocery > Juice > Cocktail Mix',
'Deli > Liq.Cream > coffeemate',
'Grocery > ConcentrateJuice',
'Deli > Fish Cake > Crab Meat',
'Frozen > Frz Bun-Plain > Dough',
'Deli > Dried',
'Deli > Duck',
'Deli > Wheat > Egg Noodle',
'Frozen > Frz Dim Sum > Egg Roll',
'Deli > Fish Cake',
'Frozen > Frozen Meat',
'Frozen > Frozen Noodle',
'Frozen > Frozen Seafood',
'Frozen > Frz  Dessert',
'Frozen > Frz Bun (salty)',
'Frozen > Frz Bun (Sweet)',
'Frozen > Frz Bun-Plain',
'Frozen > Frz Dim Sum',
'Frozen > Frz Dumpling',
'Frozen > Frz Fruit',
'Frozen > Frz Instant Meal',
'Frozen > Frz Instant Noodle',
'Frozen > Frz Instant Rice',
'Frozen > FRZ MOON CAKE',
'Frozen > Frz Pancake',
'Frozen > Frz Rice Ball',
'Frozen > Frz Rice Cake&Noodle',
'Frozen > Frz Vegetarian Food',
'Frozen > Frz Wrapper',
'Frozen > FrzJuice <50%juice',
'Deli > Gelatin',
'Deli > Bean cake > Gluten',
'Deli > Sausage > Hot Dog > Ham',
'Deli > Sausage > Hot Dog',
'Frozen > Ice Cream',
'Grocery > Juice',
'Deli > Juice',
'Deli > Liq.Cream',
'Deli > Butter > Margarin',
'Deli > Meat Ball',
'Deli > Meat Ball > Meat Paste',
'Deli > Milk',
'Deli > Miso',
'Deli > Cake > Pancake',
'Deli > Seafood ball > Paste',
'Grocery > Seafood Sauce > Paste',
'Deli > Pickled Vegetable',
'Frozen > Ice Cream > Popsicle',
'Frozen > Popsicle-Juice<=50%',
'Deli > Preserved Egg',
'Deli > Gelatin > Pudding',
'Deli > Juice > Punch',
'Deli > Duck > Quail',
'Deli > Ready to Eat Meal',
'Deli > Rice cake',
'Deli > Rice Noodle',
'Deli > Rice Noodle > RiceRoll',
'Deli > Salted Egg',
'Deli > Salted Meat',
'Deli > Dried > Salted Seafood',
'Deli > Sausage',
'Deli > Salted Meat > Sausage',
'Deli > Seafood ball',
'Grocery > Seafood Sauce',
'Grocery > Seasoning Sauce',
'Deli > Soymilk',
'Grocery > Chili Sauce > Sweet',
'Deli > Sweet Dessert',
'Deli > Tofu Deli',
'Deli > Udon',
'Frozen > Frz Fruit > Vegetable',
'Deli > Vegetarian food',
'Grocery > ConcentrateJuice > Vin',
'Frozen > Frz Pancake > Waffle',
'Grocery > Water',
'Deli > Wheat',
'Deli > White',
'Deli > Wrapper > Wonton Skin',
'Deli > Wrapper',
'Deli > Yam Cake Konnyaku'
}
MS_set = {
    'Meat > Beef',
'Meat > Chicken',
'Seafood > Cooked Shrimp Frozen',
'Seafood > Crab',
'Seafood > Crab Frozen',
'Meat > Duck',
'Seafood > Fish Ball Frozen',
'Seafood > Fish Fillet Frozen',
'Seafood > Fish Steak',
'Seafood > Fish Steak Frozen',
'Seafood > Frog Leg Frozen',
'Meat > Geese',
'Meat > Goat',
'Seafood > Imitation Crab meat',
'Meat > Goat > Lamb',
'Meat',
'Seafood > Mixed Seafood Frozen',
'Seafood > Octopus Frozen',
'Meat > Beef > Ox',
'Meat > Partridge',
'Meat > Pork > Pig',
'Meat > Pork',
'Meat > Quail',
'Seafood > Roe Frozen',
'Seafood > Sashimi',
'Seafood > Scallop Frozen',
'Seafood',
'Seafood > Seafood Cucumber Frz',
'Seafood > Shellfish',
'Seafood > Shellfish Frozen',
'Seafood > Shrimp',
'Seafood > Shrimp Frozen',
'Meat > Squab',
'Seafood > Squid Frozen',
'Meat > Turkey',
'Seafood > Whole Fish',
'Seafood > Whole Fish Frozen'
}
old_repeat = set()
GD106_repeat = set()
GL101_repeat = set()
BCKHD_repeat = set()
GF103_repeat = set()
MS_repeat = set()
# 存储前台类目范围
template_range = {1 : [71,86],2:[212,227],3 : [228,242,629],4:[243,258],5 : [1,14]}
# template_range = {1 : [71,86],2:[212,227],3 : [228,242,629],4:[243,258]}

# 前台有些类目不在8899的模板里
template_cv = {5 : {'Appliances','Cleaning'}}

#只存储绑定前后台id的query
listQ2 =[]
depDict = {"10": "Grocery", "20": "Meat", "30": "Produce", "40": "Seafood", "50": "Bakery", "60": "Deli"}
rateDict = {"10": "0", "20": "5", "30": "5", "40": "5", "50": "0", "60": "0"}
# 存储所有父类目（一级类目）的雪花ID
# 存储所有mch
pcidDict = {}
set_mch = set()
set_path = set()
set_pair = set()
q1 = "insert into tawa_2_product.pms_category "
q2 = "(parent_id,name,parent_name,level,path,is_last,is_leaf,surcharge_rate,status,updated_by,created_by,updated_by_name,created_by_name,sort) values"
q4 = f"insert into tawa_2_product.pms_category_view_relation (category_view_id,category_id) values "

parentSort, levels = 100, 1
isLast, isLeaf, status, updatedby, createdby, updatedbyname, createdbyname = "1", "0", "0", "-1", "-1", "RD", "RD"

# Count1 = 带slash的category name
count1 = 0
for key, value in depDict.items():
    if value == 'Produce':
        name, pname, level, path, rate, sort = value, "", str(levels), value, rateDict[key], str(parentSort)
        parentSort += 1
        q3 = f"(0, '{name}', '{pname}', {level}, '{path}', {isLast}, {isLeaf}, {rate}, {status}, {updatedby}, {createdby}, '{updatedbyname}', '{createdbyname}', {sort});\n"
        q = q1 + q2 + q3
        listQ.append(q)
        set_path.add(path)

for key, value in depDict.items():
    pcid = "@parentId" + value
    if value == 'Produce':
        q = f"SET {pcid} = (SELECT id FROM tawa_2_product.pms_category WHERE name = '{value}' and level = 1 and updated_by_name = \"RD\" and created_by_name = \"RD\" LIMIT 1);\n\n"
    else:
        q = f"SET {pcid} = (SELECT id FROM tawa_2_product.pms_category WHERE name = '{value}' and level = 1 and updated_by_name != \"RD\" and created_by_name != \"RD\" LIMIT 1);\n\n" 
    listQ.append(q)
    pcidDict[key] = pcid

# 写入父类目的Query到文本文件
with open(txt_file_path, mode='w', encoding='utf-8') as txt_file:
    for q in listQ:
        txt_file.write(q)

listQ.clear()  # 清空listQ以便后续使用

levels += 1
childIdx = 0

# 处理子类目的Query
with open(csv_file_path, mode='r', encoding='utf-8-sig', newline='') as file:
    reader = csv.reader(file)
    for index, row in enumerate(reader):
        i = 0
        levels = 2
        if index == 0 or row[11] == "" or row[11] in set_mch:
            continue
        # if index > 12:
        #     break
        set_mch.add(row[11])
        mchFirst2 = str(row[11][:2])
        mchFirst3 = str(row[11][:3])
        mchname = row[12]
        pcid, name, pname, level, path, rate, sort = "", "", "", str(levels), depDict[mchFirst2], rateDict[mchFirst2], str(i)
        tempQ = []
        if '/' in mchname:
            l = mchname.split('/')
            for idx, item in enumerate(l):
                if idx == 0:
                    pcid = "@parentId" +str(index)+ str(idx)
                    name, pname, path = l[idx], depDict[mchFirst2], path + " > " + l[idx]
                    if path in pcidDict:
                        continue
                    q3 = f"({pcidDict.get(mchFirst2)}, '{name}', '{pname}', {level}, '{path}', {isLast}, {isLeaf}, {rate}, {status}, {updatedby}, {createdby}, '{updatedbyname}', '{createdbyname}', {sort});\n"
                    q = q1 + q2 + q3
                    tempQ.append(q)
                    q = f"SET {pcid} = (SELECT id FROM tawa_2_product.pms_category WHERE name = \"{l[idx]}\" AND level = \"{str(levels)}\" AND updated_by_name = \"RD\" AND created_by_name = \"RD\" LIMIT 1);\n"
                    pcidDict[path] = pcid
                    tempQ.append(q)
                    levels += 1
                    i += 1
                    if path in GL101_set:
                        GL101_repeat.add(path)
                    elif path in GD106_set:
                        GD106_repeat.add(path)
                    elif path in BCKHD_set:
                        BCKHD_repeat.add(path)
                    elif path in GF103_set:
                        GF103_repeat.add(path)
                    elif path in MS_set:
                        MS_repeat.add(path)
                    
                    if path in old_set:
                        old_repeat.add(path)
                else:
                    
                    pcid,pname, name, level, path, sort = pcidDict[path],name, l[idx], levels, path + " > " + l[idx], str(i)
                    if path in pcidDict:
                        continue
                    q3 = f"({pcid}, '{name}', '{pname}', {level}, '{path}', {isLast}, {isLeaf}, {rate}, {status}, {updatedby}, {createdby}, '{updatedbyname}', '{createdbyname}', {sort});\n\n"
                    q = q1 + q2 + q3
                    tempQ.append(q)
                    pcid = "@parentId" +str(index)+ str(idx)
                    q = f"SET {pcid} = (SELECT id FROM tawa_2_product.pms_category WHERE name = \"{l[idx]}\" AND level = \"{str(levels)}\" AND updated_by_name = \"RD\" AND created_by_name = \"RD\" LIMIT 1);\n\n"
                    pcidDict[path] = pcid
                    tempQ.append(q)
                    levels += 1
                    i += 1
                    if path in GL101_set:
                        GL101_repeat.add(path)
                    elif path in GD106_set:
                        GD106_repeat.add(path)
                    elif path in BCKHD_set:
                        BCKHD_repeat.add(path)
                    elif path in GF103_set:
                        GF103_repeat.add(path)
                    elif path in MS_set:
                        MS_repeat.add(path)
                    if path in old_set:
                        old_repeat.add(path)

            count1+=1
        else:
            name, pname, path = row[12], depDict[mchFirst2], path + " > " + row[12]
            if path in set_path:
                continue
            q3 = f"({pcidDict.get(mchFirst2)}, '{name}', '{pname}', {level}, '{path}', {isLast}, {isLeaf}, {rate}, {status}, {updatedby}, {createdby}, '{updatedbyname}', '{createdbyname}', {sort});\n"
            q = q1 + q2 + q3
            tempQ.append(q)
            pcid = "@parentId" + str(index)
            q = f"SET {pcid} = (SELECT id FROM tawa_2_product.pms_category WHERE name = \"{name}\" AND level = \"{str(levels)}\" AND updated_by_name = \"RD\" AND created_by_name = \"RD\" LIMIT 1);\n\n"
            pcidDict[path] = pcid
            tempQ.append(q)
            if path in GL101_set:
                GL101_repeat.add(path)
            elif path in GD106_set:
                GD106_repeat.add(path)
            elif path in BCKHD_set:
                BCKHD_repeat.add(path)
            elif path in GF103_set:
                GF103_repeat.add(path)
            elif path in MS_set:
                MS_repeat.add(path)
            if path in old_set:
                old_repeat.add(path)
        if mchFirst2 == "50" or mchFirst2 == "60":
            listQ_5 += tempQ
            listQ_5.append("\n")
        elif mchFirst2 == "40" or mchFirst2 == "20":
            listQ_7 += tempQ
            listQ_7.append("\n")
        elif mchFirst2 == "30":
            listQ_1 += tempQ
            listQ_1.append("\n")
        else:
            if mchFirst3 == "103" or mchFirst3 == "104":
                listQ_6 += tempQ
                listQ_6.append("\n")
            elif mchFirst3 == "101":
                listQ_3 += tempQ
                listQ_3.append("\n")
            elif mchFirst3 == "105":
                listQ_2 += tempQ
                listQ_2.append("\n")
            elif mchFirst3 == "106":
                listQ_4 += tempQ
                listQ_4.append("\n")
        
listQ_1.append("-- -----------------------------------------category view - Prod Final-----------------------------------------\n")
listQ_2.append("-- -----------------------------------------category view - Prod Final-----------------------------------------\n")
listQ_3.append("-- -----------------------------------------category view - Prod Final-----------------------------------------\n")
listQ_4.append("-- -----------------------------------------category view - Prod Final-----------------------------------------\n")
listQ_5.append("-- -----------------------------------------category view - Prod Final-----------------------------------------\n")
listQ_6.append("-- -----------------------------------------category view - Prod Final-----------------------------------------\n")
listQ_7.append("-- -----------------------------------------category view - Prod Final-----------------------------------------\n")

print("With left slash： " + str(count1))
print(pcidDict["Grocery > Yogurt Drink"])
if len(GL101_repeat) == 0:
    print("no repeat for GL105")   
else:
    print("GL105")
    print(GL101_repeat)   

if len(GD106_repeat) == 0:
    print("no repeat for GD106")   
else:
    print("GD106") 
    print(GD106_repeat)  

if len(BCKHD_repeat) == 0:
    print("no repeat for BCKHD")   
else:
    print("BCKHD") 
    print(BCKHD_repeat)  

if len(GF103_repeat) == 0:
    print("no repeat for GF103")   
else:
    print("GF103")  
    print(GF103_repeat)  

if len(MS_repeat) == 0:
    print("no repeat for MS")   
else:
    print("MS")   
    print(MS_repeat)     

print("Old path for reference")   
print(old_repeat) 
# 前后台id绑定
#前台2级类目
#如果有slice的话，后台
with open(csv_file_path, mode='r', encoding='utf-8-sig', newline='') as file:
    reader = csv.reader(file)
    for index, row in enumerate(reader):
        if index == 0 or row[11] == "":
            continue
        if row[5] == "":
            print("Some record have issue")
        categoryview_id = "@cvid" + str(index)
        mchFirst2 = str(row[11][:2])
        mchFirst3 = str(row[11][:3])
        path = depDict[mchFirst2]
        tempQ = []
        mchname = row[12]
        # 前后台的pair必须唯一；发现重复直接continue
        #生成前台类目的全局变量
        q5 = f"SET {categoryview_id} = (SELECT id FROM tawa_2_product.pms_category_view WHERE name_EN = '{row[5]}' AND parent_id >= 634 AND parent_id <= 650 LIMIT 1);\n"
        tempQ.append(q5)
        if '/' in mchname:
            # 前后台类目的pair必须唯一 (前台Level2 + path)；发现重复直接continue (这边会对接到最底层类目)
            l = mchname.split('/')
            temp = ""
            for idx, item in enumerate(l):
                pair = row[4] + "+" + path + "+" + item
                if pair in set_pair:
                    continue
                set_pair.add(pair)
                category_id = "@cid" +str(index)+str(idx)
                name,parentname,level = item, depDict[mchFirst2] if idx == 0 else temp,idx+2
                q6 = f"SET {category_id} = (SELECT id FROM tawa_2_product.pms_category WHERE name = '{name}' AND parent_name = '{parentname}' AND level = {level} AND updated_by_name = 'RD' AND created_by_name = 'RD' LIMIT 1);\n"
                tempQ.append(q6)
                q7 = q4 + f"({categoryview_id},{category_id});\n"
                tempQ.append(q7)
                temp = item
        else:
            # 前后台类目的pair必须唯一(前台Level2 + path)；发现重复直接continue
            pair = row[4] + "+" + path + "+" + mchname
            if pair in set_pair:
                continue
            set_pair.add(pair)
            category_id = "@cid" +str(index)
            name,parentname,level = mchname, depDict[mchFirst2],2
            q6 = f"SET {category_id} = (SELECT id FROM tawa_2_product.pms_category WHERE name = '{name}' AND parent_name = '{parentname}' AND level = {level} AND updated_by_name = 'RD' AND created_by_name = 'RD' LIMIT 1);\n"
            q7 = q4 + f"({categoryview_id},{category_id});\n"
            tempQ.append(q6)
            tempQ.append(q7)
        tempQ.append("\n")

        if mchFirst2 == "50" or mchFirst2 == "60":
            listQ_5 += tempQ
            listQ_5.append("\n")
        elif mchFirst2 == "40" or mchFirst2 == "20":
            listQ_7 += tempQ
            listQ_7.append("\n")
        elif mchFirst2 == "30":
            listQ_1 += tempQ
            listQ_1.append("\n")
        else:
            if mchFirst3 == "103" or mchFirst3 == "104":
                listQ_6 += tempQ
                listQ_6.append("\n")
            elif mchFirst3 == "101":
                listQ_3 += tempQ
                listQ_3.append("\n")
            elif mchFirst3 == "105":
                listQ_2 += tempQ
                listQ_2.append("\n")
            elif mchFirst3 == "106":
                listQ_4 += tempQ
                listQ_4.append("\n")
listQ_1.append("-- -----------------------------------------Old CV to New C-----------------------------------------\n")
listQ_2.append("-- -----------------------------------------Old CV to New C-----------------------------------------\n")
listQ_3.append("-- -----------------------------------------Old CV to New C-----------------------------------------\n")
listQ_4.append("-- -----------------------------------------Old CV to New C-----------------------------------------\n")
listQ_5.append("-- -----------------------------------------Old CV to New C-----------------------------------------\n")
listQ_6.append("-- -----------------------------------------Old CV to New C-----------------------------------------\n")

# 旧的前台对应新的后台
# 此处需要读取mch2
with open(csv_file_path_2, mode='r', encoding='utf-8-sig', newline='') as file:
    reader = csv.reader(file)
    for index, row in enumerate(reader):
        if index == 0 or row[9] == "" or len(row[9]) < 8:
            continue
       
        mchFirst2 = str(row[9][:2])
        mchFirst3 = str(row[9][:3])
        path = depDict[mchFirst2]
        tempQ = []
        tempQ2=[]
        mchname = row[10]
        # 前后台的pair必须唯一；发现重复直接continue
        #遍历模板生成前台类目的全局变量
        for key, value in template_range.items():
            categoryview_id = "@cvid_" + str(index) +"_"+ str(key)
            q5 = ""
            q55 = ""
            if key == 3:
                q5 = f"SET {categoryview_id} = (SELECT id FROM tawa_2_product.pms_category_view WHERE parent_name_EN = '{row[0]}' AND name_EN = '{row[3]}' AND parent_id >= {value[0]} AND parent_id <= {value[1]} or parent_id = {value[2]} LIMIT 1);\n"
                q55 = f"SELECT id FROM tawa_2_product.pms_category_view WHERE name_EN = '{row[3]}' AND parent_id >= {value[0]} AND parent_id <= {value[1]} or parent_id = {value[2]} LIMIT 1;\n"
            elif key == 5 and row[3] in template_cv[5]:
                q5 = f"SET {categoryview_id} = (SELECT id FROM tawa_2_product.pms_category_view WHERE parent_name_EN = '{row[0]}' AND name_EN = '{row[3]}' AND parent_id >= {value[0]} AND parent_id <= {value[1]} LIMIT 1);\n"
                q55 = f"SELECT id FROM tawa_2_product.pms_category_view WHERE name_EN = '{row[3]}' AND parent_id >= {value[0]} AND parent_id <= {value[1]} LIMIT 1;\n"
            elif key != 5 and key != 3:
                q5 = f"SET {categoryview_id} = (SELECT id FROM tawa_2_product.pms_category_view WHERE parent_name_EN = '{row[0]}' AND name_EN = '{row[3]}' AND parent_id >= {value[0]} AND parent_id <= {value[1]} LIMIT 1);\n"
                q55 = f"SELECT id FROM tawa_2_product.pms_category_view WHERE name_EN = '{row[3]}' AND parent_id >= {value[0]} AND parent_id <= {value[1]} LIMIT 1;\n"
            if key == 5 and row[3] not in template_cv[5]:
                continue
            tempQ.append(q5)
            tempQ2.append(q55)
            if '/' in mchname:
                # 前后台类目的pair必须唯一 (前台Level2 + path)；发现重复直接continue (这边会对接到最底层类目)
                l = mchname.split('/')
                temp = ""
                for idx, item in enumerate(l):
                    pair = row[3] + "_" + path + "_" + item + "_" + str(key)
                    if pair in set_pair:
                        continue
                    set_pair.add(pair)
                    category_id = "@cid" +str(index)+str(idx)
                    name,parentname,level = item, depDict[mchFirst2] if idx == 0 else temp,idx+2
                    q6 = f"SET {category_id} = (SELECT id FROM tawa_2_product.pms_category WHERE name = '{name}' AND parent_name = '{parentname}' AND level = {level} AND updated_by_name = 'RD' AND created_by_name = 'RD' LIMIT 1);\n"
                    tempQ.append(q6)
                    q7 = q4 + f"({categoryview_id},{category_id});\n"
                    tempQ.append(q7)
                    temp = item
            else:
                # 前后台类目的pair必须唯一(前台Level2 + path)；发现重复直接continue
                pair = row[3] + "_" + path + "_" + mchname + "_" + str(key)
                if pair in set_pair:
                    continue
                set_pair.add(pair)
                category_id = "@cid" +str(index)
                name,parentname,level = mchname, depDict[mchFirst2],2
                q6 = f"SET {category_id} = (SELECT id FROM tawa_2_product.pms_category WHERE name = '{name}' AND parent_name = '{parentname}' AND level = {level} AND updated_by_name = 'RD' AND created_by_name = 'RD' LIMIT 1);\n"
                tempQ.append(q6)
                q7 = q4 + f"({categoryview_id},{category_id});\n"
                tempQ.append(q7)
            tempQ.append("\n")

        if mchFirst2 == "50" or mchFirst2 == "60":
            listQ_5 += tempQ
            listQ_5.append("\n")
            listQ_51 += tempQ2
            listQ_51.append("\n")
        elif mchFirst2 == "40" or mchFirst2 == "20":
            listQ_7 += tempQ
            listQ_7.append("\n")
            listQ_71 += tempQ2
            listQ_71.append("\n")
        elif mchFirst2 == "30":
            listQ_1 += tempQ
            listQ_1.append("\n")
            listQ_11 += tempQ2
            listQ_11.append("\n")
        else:
            if mchFirst3 == "103" or mchFirst3 == "104":
                listQ_6 += tempQ
                listQ_6.append("\n")
                listQ_61 += tempQ2
                listQ_61.append("\n")
            elif mchFirst3 == "101":
                listQ_3 += tempQ
                listQ_3.append("\n")
                listQ_31 += tempQ2
                listQ_31.append("\n")
            elif mchFirst3 == "105":
                listQ_2 += tempQ
                listQ_2.append("\n")
                listQ_21 += tempQ2
                listQ_21.append("\n")
            elif mchFirst3 == "106":
                listQ_4 += tempQ
                listQ_4.append("\n")
                listQ_41 += tempQ2
                listQ_41.append("\n")





# 写入子类目的Query到文本文件
with open(txt_file_path_1, mode='a', encoding='utf-8') as txt_file:
    txt_file.write("-- -----------------------------------------Produce-----------------------------------------\n")
    for q in listQ_1:
        txt_file.write(q)
    txt_file.write("-- -----------------------------------------Produce End-----------------------------------------\n")
    for q in listQ_11:
        txt_file.write(q)
with open(txt_file_path_2, mode='a', encoding='utf-8') as txt_file:
    txt_file.write("-- -----------------------------------------Grocery Non Food 105-----------------------------------------\n")
    for q in listQ_2:
        txt_file.write(q)
    txt_file.write("-- -----------------------------------------Grocery Non Food 105-----------------------------------------\n")
    for q in listQ_21:
        txt_file.write(q)
with open(txt_file_path_3, mode='a', encoding='utf-8') as txt_file:
    txt_file.write("-- -----------------------------------------Grocery Leisure 101-----------------------------------------\n")
    for q in listQ_3:
        txt_file.write(q)
    txt_file.write("-- -----------------------------------------Grocery Leisure 101 end-----------------------------------------\n")
    for q in listQ_31:
        txt_file.write(q)
with open(txt_file_path_4, mode='a', encoding='utf-8') as txt_file:
    txt_file.write("-- -----------------------------------------Grocery Dry 106-----------------------------------------\n")
    for q in listQ_4:
        txt_file.write(q)
    txt_file.write("-- -----------------------------------------Grocery Dry 106 end-----------------------------------------\n")
    for q in listQ_41:
        txt_file.write(q)
with open(txt_file_path_5, mode='a', encoding='utf-8') as txt_file:
    txt_file.write("-- -----------------------------------------BCK/Hot Deli-----------------------------------------\n")
    for q in listQ_5:
        txt_file.write(q)
    txt_file.write("-- -----------------------------------------BCK/Hot Deli end-----------------------------------------\n")
    for q in listQ_51:
        txt_file.write(q)
with open(txt_file_path_6, mode='a', encoding='utf-8') as txt_file:
    txt_file.write("-- -----------------------------------------Grocery Frozen & Deli (103 & 104)-----------------------------------------\n")
    for q in listQ_6:
        txt_file.write(q)
    txt_file.write("-- -----------------------------------------Grocery Frozen & Deli (103 & 104) end-----------------------------------------\n")
    for q in listQ_61:
        txt_file.write(q)
with open(txt_file_path_7, mode='a', encoding='utf-8') as txt_file:
    txt_file.write("-- -----------------------------------------Meat & Seafood-----------------------------------------\n")
    for q in listQ_7:
        txt_file.write(q)
    txt_file.write("-- -----------------------------------------Meat & Seafood end-----------------------------------------\n")
    for q in listQ_71:
        txt_file.write(q)


        
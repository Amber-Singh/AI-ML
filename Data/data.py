import uuid

sample_recipes = [
        {
            "id": "5c82bb4d-df72-4d00-b8a7-01b30f436a21",
            "name": "Classic Spaghetti Carbonara",
            "cuisine": "Italian",
            "ingredients": [
                "400g spaghetti",
                "200g pancetta or guanciale",
                "4 large eggs",
                "100g Pecorino Romano cheese",
                "Black pepper",
                "Salt"
            ],
            "instructions": """
            1. Bring a large pot of salted water to boil and cook spaghetti until al dente
            2. Meanwhile, cut pancetta into small cubes and fry until crispy
            3. In a bowl, whisk eggs with grated Pecorino and black pepper
            4. Drain pasta, reserving 1 cup of pasta water
            5. Add hot pasta to pancetta, remove from heat
            6. Quickly stir in egg mixture, adding pasta water to create creamy sauce
            7. Serve immediately with extra cheese and pepper
            """,
            "cooking_time": "20 minutes",
            "prep_time": "10 minutes",
            "difficulty": "Medium",
            "servings": "4",
            "calories_per_serving": "520",
            "dietary_info": "Contains eggs, dairy, pork",
            "tips": "The key is to add eggs off heat to avoid scrambling. Use pasta water to achieve perfect creaminess."
        },
        {
            "id": "e6f649ef-c3d4-4772-8d72-8c2863fb6206",
            "name": "Thai Green Curry",
            "cuisine": "Thai",
            "ingredients": [
                "2 tbsp green curry paste",
                "400ml coconut milk",
                "300g chicken breast, sliced",
                "1 eggplant, cubed",
                "100g green beans",
                "2 kaffir lime leaves",
                "1 tbsp fish sauce",
                "1 tsp palm sugar",
                "Thai basil leaves",
                "Jasmine rice for serving"
            ],
            "instructions": """
            1. Heat 2 tbsp of coconut cream in a wok, add curry paste and fry until fragrant
            2. Add chicken and cook until sealed
            3. Pour in remaining coconut milk and bring to simmer
            4. Add eggplant, beans, lime leaves, fish sauce, and sugar
            5. Simmer for 15 minutes until vegetables are tender
            6. Stir in Thai basil leaves
            7. Serve hot with jasmine rice
            """,
            "cooking_time": "25 minutes",
            "prep_time": "15 minutes",
            "difficulty": "Medium",
            "servings": "4",
            "calories_per_serving": "380",
            "dietary_info": "Contains fish sauce, coconut. Can be made vegetarian.",
            "tips": "Adjust spice level by using less curry paste. Add bamboo shoots for extra texture."
        },
        {
            "id": "84ec86eb-f6fe-48d3-97ad-44f6ae45ac20",
            "name": "Classic Margherita Pizza",
            "cuisine": "Italian",
            "ingredients": [
                "Pizza dough (500g)",
                "200ml tomato sauce",
                "300g fresh mozzarella",
                "Fresh basil leaves",
                "2 tbsp olive oil",
                "Salt",
                "Flour for dusting"
            ],
            "instructions": """
            1. Preheat oven to 250°C (480°F) with pizza stone if available
            2. Roll out pizza dough on floured surface to 12-inch circle
            3. Spread tomato sauce evenly, leaving 1-inch border
            4. Tear mozzarella and distribute over sauce
            5. Drizzle with olive oil and sprinkle salt
            6. Bake for 10-12 minutes until crust is golden and cheese bubbles
            7. Top with fresh basil leaves and serve immediately
            """,
            "cooking_time": "12 minutes",
            "prep_time": "20 minutes",
            "difficulty": "Easy",
            "servings": "2",
            "calories_per_serving": "450",
            "dietary_info": "Vegetarian. Contains gluten and dairy.",
            "tips": "For crispier crust, use pizza stone. Let dough rest at room temperature 30 minutes before shaping."
        },
        {
            "id": "f4cf72c5-6828-41cf-a696-9dad322f0124",
            "name": "Chicken Tikka Masala",
            "cuisine": "Indian",
            "ingredients": [
                "500g chicken breast, cubed",
                "200g yogurt",
                "2 tbsp tikka masala paste",
                "400g canned tomatoes",
                "200ml heavy cream",
                "2 onions, diced",
                "4 cloves garlic, minced",
                "1 inch ginger, grated",
                "2 tsp garam masala",
                "1 tsp turmeric",
                "Fresh cilantro",
                "Basmati rice for serving"
            ],
            "instructions": """
            1. Marinate chicken in yogurt and 1 tbsp tikka paste for 30 minutes
            2. Grill or pan-fry chicken until charred, set aside
            3. In same pan, sauté onions until golden
            4. Add garlic, ginger, remaining tikka paste, and spices
            5. Add tomatoes and simmer for 10 minutes
            6. Blend sauce until smooth (optional for creamier texture)
            7. Return sauce to pan, add chicken and cream
            8. Simmer for 10 minutes, garnish with cilantro
            9. Serve with basmati rice and naan bread
            """,
            "cooking_time": "35 minutes",
            "prep_time": "40 minutes (including marination)",
            "difficulty": "Medium",
            "servings": "4",
            "calories_per_serving": "420",
            "dietary_info": "Contains dairy. Gluten-free without naan.",
            "tips": "Marinate longer for deeper flavor. Add kasuri methi (dried fenugreek) for authentic taste."
        },
        {
            "id": "1b3f6846-28a1-4f87-9974-8455d0312250",
            "name": "Caesar Salad",
            "cuisine": "American",
            "ingredients": [
                "2 romaine lettuce heads",
                "100g Parmesan cheese",
                "2 cups croutons",
                "4 anchovy fillets",
                "2 egg yolks",
                "2 cloves garlic",
                "1 tbsp Dijon mustard",
                "2 tbsp lemon juice",
                "150ml olive oil",
                "Salt and black pepper"
            ],
            "instructions": """
            1. Wash and tear romaine lettuce into bite-sized pieces
            2. Make dressing: blend anchovies, garlic, mustard, egg yolks, and lemon juice
            3. Slowly drizzle olive oil while blending until emulsified
            4. Season dressing with salt and pepper
            5. Toss lettuce with dressing until evenly coated
            6. Top with shaved Parmesan and croutons
            7. Serve immediately
            """,
            "cooking_time": "0 minutes",
            "prep_time": "15 minutes",
            "difficulty": "Easy",
            "servings": "4",
            "calories_per_serving": "320",
            "dietary_info": "Contains eggs, dairy, fish (anchovies). Gluten in croutons.",
            "tips": "Use pasteurized eggs for safety. Add grilled chicken for a complete meal."
        },
        {
            "id": "a34fbddb-c4e9-484e-b19e-0338273a5a96",
            "name": "Vegetable Stir-Fry",
            "cuisine": "Chinese",
            "ingredients": [
                "2 cups broccoli florets",
                "1 red bell pepper, sliced",
                "1 cup snap peas",
                "1 carrot, julienned",
                "2 cloves garlic, minced",
                "1 inch ginger, grated",
                "3 tbsp soy sauce",
                "1 tbsp oyster sauce",
                "1 tsp sesame oil",
                "2 tbsp vegetable oil",
                "1 tsp cornstarch",
                "Sesame seeds for garnish"
            ],
            "instructions": """
            1. Mix soy sauce, oyster sauce, sesame oil, and cornstarch for sauce
            2. Heat wok or large pan over high heat with vegetable oil
            3. Add garlic and ginger, stir-fry for 30 seconds
            4. Add harder vegetables (broccoli, carrots) first, stir-fry 2 minutes
            5. Add bell pepper and snap peas, stir-fry 2 more minutes
            6. Pour sauce over vegetables, toss until glossy
            7. Garnish with sesame seeds and serve with rice or noodles
            """,
            "cooking_time": "10 minutes",
            "prep_time": "15 minutes",
            "difficulty": "Easy",
            "servings": "4",
            "calories_per_serving": "150",
            "dietary_info": "Vegan option available (skip oyster sauce). Gluten-free with tamari.",
            "tips": "Keep heat high and vegetables moving. Don't overcrowd the pan for best texture."
        },
        {
            "id": "e22987c7-c9de-41c5-8d54-9c16d2a34f96",
            "name": "Beef Tacos",
            "cuisine": "Mexican",
            "ingredients": [
                "500g ground beef",
                "1 onion, diced",
                "2 cloves garlic, minced",
                "2 tsp cumin",
                "2 tsp paprika",
                "1 tsp chili powder",
                "Salt and pepper",
                "8 taco shells or tortillas",
                "Shredded lettuce",
                "Diced tomatoes",
                "Shredded cheese",
                "Sour cream",
                "Salsa",
                "Lime wedges"
            ],
            "instructions": """
            1. Heat oil in pan and sauté onions until soft
            2. Add garlic and cook for 1 minute
            3. Add ground beef, breaking it up as it cooks
            4. When beef is browned, add spices and season with salt and pepper
            5. Add 1/4 cup water and simmer for 5 minutes
            6. Warm taco shells according to package instructions
            7. Fill shells with beef mixture
            8. Top with lettuce, tomatoes, cheese, sour cream, and salsa
            9. Serve with lime wedges
            """,
            "cooking_time": "20 minutes",
            "prep_time": "15 minutes",
            "difficulty": "Easy",
            "servings": "4",
            "calories_per_serving": "380",
            "dietary_info": "Contains dairy. Gluten-free with corn tortillas.",
            "tips": "Make it healthier with ground turkey. Add black beans for extra protein and fiber."
        },
        {
            "id": "18440cff-bf14-4032-8c20-7ad4185606d3",
            "name": "Mushroom Risotto",
            "cuisine": "Italian",
            "ingredients": [
                "300g arborio rice",
                "300g mixed mushrooms, sliced",
                "1 onion, finely diced",
                "2 cloves garlic, minced",
                "150ml white wine",
                "1 liter hot vegetable stock",
                "50g butter",
                "100g Parmesan cheese",
                "2 tbsp olive oil",
                "Fresh parsley",
                "Salt and pepper"
            ],
            "instructions": """
            1. Heat olive oil and half the butter in large pan
            2. Sauté mushrooms until golden, season and set aside
            3. In same pan, cook onion until soft, add garlic
            4. Add rice and stir for 2 minutes until translucent
            5. Pour in wine and stir until absorbed
            6. Add hot stock one ladle at a time, stirring constantly
            7. Continue adding stock as each ladle is absorbed (18-20 minutes)
            8. When rice is creamy but al dente, stir in remaining butter, Parmesan, and mushrooms
            9. Season and garnish with parsley
            """,
            "cooking_time": "30 minutes",
            "prep_time": "10 minutes",
            "difficulty": "Medium",
            "servings": "4",
            "calories_per_serving": "420",
            "dietary_info": "Vegetarian. Contains dairy. Gluten-free.",
            "tips": "Stir constantly for creamiest texture. Rice should be creamy but still have slight bite."
        },
        {
            "id": "8f35e1df-c939-4c93-8070-45d431f82cf1",
            "name": "Greek Salad",
            "cuisine": "Greek",
            "ingredients": [
                "4 tomatoes, cut into wedges",
                "1 cucumber, sliced",
                "1 red onion, thinly sliced",
                "200g feta cheese, cubed",
                "100g Kalamata olives",
                "1 green bell pepper, sliced",
                "4 tbsp olive oil",
                "2 tbsp red wine vinegar",
                "1 tsp dried oregano",
                "Salt and pepper"
            ],
            "instructions": """
            1. Cut tomatoes into wedges and cucumber into thick slices
            2. Slice onion and bell pepper thinly
            3. Combine vegetables in large bowl
            4. Add olives and feta cheese cubes
            5. In small bowl, whisk olive oil, vinegar, oregano, salt, and pepper
            6. Pour dressing over salad
            7. Toss gently to combine
            8. Let sit for 10 minutes for flavors to meld
            9. Serve at room temperature with pita bread
            """,
            "cooking_time": "0 minutes",
            "prep_time": "15 minutes",
            "difficulty": "Easy",
            "servings": "4",
            "calories_per_serving": "220",
            "dietary_info": "Vegetarian. Contains dairy (feta). Gluten-free.",
            "tips": "Use the ripest tomatoes for best flavor. Don't overdress - Greek salad should be light."
        },
        {
            "id": "58bee054-8ac4-4f4f-9d02-bffa1bdf9cf0",
            "name": "Pad Thai",
            "cuisine": "Thai",
            "ingredients": [
                "200g rice noodles",
                "200g shrimp or chicken",
                "2 eggs",
                "3 cloves garlic, minced",
                "100g bean sprouts",
                "3 green onions, chopped",
                "50g roasted peanuts, crushed",
                "3 tbsp fish sauce",
                "2 tbsp tamarind paste",
                "2 tbsp palm sugar",
                "1 lime",
                "Vegetable oil",
                "Chili flakes (optional)"
            ],
            "instructions": """
            1. Soak rice noodles in warm water for 30 minutes, drain
            2. Mix fish sauce, tamarind paste, and palm sugar for sauce
            3. Heat wok over high heat with oil
            4. Cook shrimp/chicken until done, remove and set aside
            5. Scramble eggs in same wok, push to side
            6. Add garlic, then drained noodles and sauce
            7. Toss everything together, add protein back in
            8. Add bean sprouts and green onions, toss briefly
            9. Serve garnished with peanuts, lime wedges, and chili flakes
            """,
            "cooking_time": "15 minutes",
            "prep_time": "35 minutes (including soaking)",
            "difficulty": "Medium",
            "servings": "2",
            "calories_per_serving": "450",
            "dietary_info": "Contains eggs, fish sauce, peanuts. Gluten-free.",
            "tips": "High heat is essential. Have all ingredients prepped before starting. Don't overcook noodles."
        },
        {
            "id": str(uuid.uuid4()),
            "name": "Butter Chicken",
            "cuisine": "Indian",
            "ingredients": [
                "1 1/2 pounds boneless chicken breast or thighs with bones",
                "2 large onions",
                "2 cloves garlic",
                "2 medium tomatoes",
                "1 tablespoon butter",
                "1 teaspoon garam masala",
                "1 teaspoon cumin powder",
                "1/2 teaspoon cayenne pepper",
                "1/2 teaspoon salt",
                "1/4 teaspoon black pepper",
                "2 tablespoons tomato puree",
                "2 tablespoons heavy cream",
                "2 tablespoons chopped fresh cilantro"
            ],
            "instructions": """1. Marinate the chicken in a mixture of yogurt and spices for at least 30 minutes.
2. Grill or cook the chicken until it is cooked through.
3. In a saucepan, melt 1 tablespoon of butter and saute the onions until they are translucent.
4. Add the garlic, ginger, and spices to the saucepan and cook for 1 minute.
5. Add the tomato puree, heavy cream, and cooked chicken to the saucepan and stir to combine.
6. Bring the mixture to a simmer and cook for 10 minutes or until the sauce has thickened.
7. Season with salt and pepper to taste.
8. Garnish with cilantro and serve over basmati rice or with naan bread.""",
            "cooking_time": "25 minutes",
            "prep_time": "20 minutes",
            "difficulty": "Medium",
            "servings": "4",
            "calories_per_serving": "420",
            "dietary_info": "Contains dairy. Gluten-free without naan.",
            "tips": "Use high quality ingredients and adjust the spice level to your liking. You can also add bell peppers or other vegetables to the sauce for added flavor."
        },
        {
            "id": str(uuid.uuid4()),
            "name": "Butter Chicken Recipe",
            "cuisine": "Western",
            "ingredients": [
                "1 pound boneless chicken breast with skin",
                "4 tablespoons unsalted butter",
                "2 cloves garlic minced",
                "1 teaspoon salt",
                "1/2 teaspoon black pepper",
                "1/2 teaspoon paprika"
            ],
            "instructions": """1. Rinse the chicken and pat dry with paper towels
2. Season the chicken with salt pepper and paprika
3. Melt 2 tablespoons of butter in a large skillet over medium heat
4. Add the chicken to the skillet and cook for 5-6 minutes per side or until cooked through
5. Remove the chicken from the skillet and set aside
6. Add the remaining 2 tablespoons of butter to the skillet
7. Add the minced garlic to the skillet and cook for 1 minute
8. Serve the chicken with the garlic butter sauce""",
            "cooking_time": "25 minutes",
            "prep_time": "15 minutes",
            "difficulty": "Easy",
            "servings": "4",
            "calories_per_serving": "320",
            "dietary_info": "Contains dairy",
            "tips": "Use high quality unsalted butter for the best flavor"
        }
    ]
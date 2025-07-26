def get_chat_response(user_message):
    user_message = user_message.strip().lower()
    
    greetings = ["hi", "hello", "hey", "hii", "helo", "vanakkam"]
    if user_message in greetings:
        return "Welcome to FARM&CO Assistant! 👋\nPlease choose a topic:\n1. 🐮 Livestock\n2. 🏥 Diseases\n3. 💰 Marketing\n4. ℹ️ Others"

    responses = {
        "what is livestock": "Livestock refers to domesticated animals raised in farms such as cows, goats, sheep, and poultry for food, milk, and other products.",
        "how to take care of cattle": "Proper cattle care includes:\n1. Clean water daily\n2. Nutritious feed\n3. Regular vet checkups\n4. Proper shelter\n5. Timely vaccinations",
        "what is the best diet for cattle": "A balanced cattle diet includes:\n1. Roughages (hay, straw)\n2. Green fodder\n3. Concentrates\n4. Minerals\n5. Fresh water",
        "how to increase milk production": "To increase milk production:\n1. Provide balanced nutrition\n2. Maintain regular milking schedule\n3. Keep stress-free environment\n4. Ensure proper hygiene\n5. Regular health checkups",
        "best cattle breeds in india": "Popular Indian cattle breeds:\n1. Gir - High milk yield\n2. Sahiwal - Heat tolerant\n3. Red Sindhi - Disease resistant\n4. Tharparkar - Adaptable\n5. Rathi - Dual purpose",
        "signs of healthy cattle": "Signs of healthy cattle:\n1. Alert and active behavior\n2. Shiny coat\n3. Regular feeding habits\n4. Normal body temperature\n5. Clear eyes and nose",
        "what is lsd": "Lumpy Skin Disease (LSD) is a viral disease causing:\n1. Skin nodules\n2. Fever\n3. Reduced milk production\n4. Loss of appetite",
        "how to prevent diseases": "Disease prevention methods:\n1. Regular vaccination\n2. Clean environment\n3. Good nutrition\n4. Pest control\n5. Regular checkups",
        "common cattle diseases": "Common cattle diseases:\n1. Foot and Mouth Disease\n2. Lumpy Skin Disease\n3. Mastitis\n4. Black Quarter\n5. Brucellosis",
        "mastitis symptoms": "Mastitis symptoms:\n1. Swollen udder\n2. Abnormal milk\n3. Reduced milk production\n4. Fever\n5. Loss of appetite",
        "vaccination schedule": "Essential vaccinations:\n1. FMD - Every 6 months\n2. HS - Annually\n3. BQ - Annually\n4. Brucellosis - Once in lifetime\n5. LSD - As per vet advice",
        "current cattle prices": "Current market rates (approx):\n1. Indigenous cow: ₹25,000-35,000\n2. Cross-bred cow: ₹45,000-60,000\n3. Buffalo: ₹40,000-50,000\nPrices vary by location and season.",
        "how to sell cattle": "Steps to sell cattle:\n1. Get health certificate\n2. List on local markets\n3. Use online platforms\n4. Contact dairy farms\n5. Approach traders",
        "milk prices": "Average milk prices:\n1. Cow milk: ₹40-50/liter\n2. Buffalo milk: ₹50-60/liter\n3. A2 milk: ₹80-100/liter",
        "dairy farming profit": "Dairy farming profitability:\n1. Income sources:\n  - Milk sales\n  - Calf sales\n  - Manure\n2. Monthly profit potential: ₹5000-15000 per cow",
        "government schemes": "Available schemes:\n1. Dairy Entrepreneurship Development\n2. National Livestock Mission\n3. DEDS subsidy scheme\n4. Rashtriya Gokul Mission",
        "insurance schemes": "Available insurance schemes:\n1. Basic cover (3% premium)\n2. Comprehensive (4.5% premium)\n3. Indigenous breeds (2.5% premium)",
        "veterinary services": "Veterinary services:\n1. 24/7 helpline: 1800-XXX-XXXX\n2. Mobile vet services\n3. Government hospitals\n4. Private clinics",
        "cattle loans": "Cattle loan options:\n1. KCC (Kisan Credit Card)\n2. NABARD schemes\n3. Commercial bank loans\n4. Micro-finance options",
        "organic farming": "Organic cattle farming:\n1. Natural feed only\n2. No antibiotics\n3. Free-range grazing\n4. Traditional medicines\n5. Better milk prices",
        "artificial insemination": "AI benefits:\n1. Better breed selection\n2. Higher success rate\n3. Disease prevention\n4. Cost-effective\n5. Available at your farm"
    }

    category_intros = {
        "livestock": "You can ask me questions about livestock care, feeding, health, and management.",
        "diseases": "Ask me about different diseases, symptoms, prevention, and treatment.",
        "marketing": "I can help with market prices, buying/selling, and trends.",
        "others": "Ask about insurance, vet services, or other general queries."
    }

    if user_message in responses:
        return responses[user_message]
    elif user_message in category_intros:
        return category_intros[user_message]
    else:
        return "Please ask a specific question about livestock care, diseases, marketing, or other related topics. You can ask about:\n1. Cattle breeds and care\n2. Common diseases\n3. Market prices\n4. Government schemes"
"""
Populate Google Sheets with Unique Health/Fitness Topics
This script adds 50+ unique, viral-worthy topics to your spreadsheet.
"""

import os
import sys
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError


# 500+ Unique Health, Fitness & Wellness Topics (Viral-Worthy)
HEALTH_FITNESS_TOPICS = [
    # Water & Hydration (20 topics)
    "7 days without sugar challenge",
    "drinking warm water on empty stomach",
    "lemon water benefits for weight loss",
    "coconut water vs sports drinks",
    "how much water to drink for glowing skin",
    "alkaline water benefits explained",
    "cucumber water for detox",
    "drinking water before bed benefits",
    "hot water vs cold water benefits",
    "water fasting 24 hours results",
    "infused water recipes for weight loss",
    "drinking water on empty stomach benefits",
    "dehydration symptoms you ignore",
    "best time to drink water",
    "water intake calculator explained",
    "sparkling water vs regular water",
    "drinking too much water dangers",
    "water retention causes and fixes",
    "electrolyte water benefits",
    "mineral water vs tap water",
    
    # Yoga & Meditation (30 topics)
    "10 minutes yoga for beginners",
    "meditation for stress relief",
    "surya namaskar benefits",
    "yoga for back pain relief",
    "breathing exercises for anxiety",
    "morning yoga routine",
    "yoga for weight loss",
    "chakra meditation guide",
    "yoga nidra for sleep",
    "pranayama breathing techniques",
    "yoga for flexibility",
    "mindfulness meditation benefits",
    "yoga poses for digestion",
    "transcendental meditation explained",
    "yoga for neck pain",
    "guided meditation for beginners",
    "yoga for better posture",
    "meditation for focus",
    "yin yoga benefits",
    "yoga for anxiety relief",
    "power yoga vs hatha yoga",
    "meditation music benefits",
    "yoga for runners",
    "loving kindness meditation",
    "yoga for seniors",
    "body scan meditation guide",
    "yoga for insomnia",
    "walking meditation technique",
    "yoga for thyroid",
    "zen meditation explained",
    
    # Weight Loss (40 topics)
    "intermittent fasting for beginners",
    "walking 10000 steps daily results",
    "green tea for fat burning",
    "best time to eat for weight loss",
    "portion control tips",
    "calorie deficit explained",
    "meal prep for weight loss",
    "keto diet for beginners",
    "carb cycling explained",
    "protein diet for fat loss",
    "apple cider vinegar weight loss",
    "HIIT workout for fat burning",
    "metabolism boosting foods",
    "weight loss plateau solutions",
    "cheat meal vs cheat day",
    "low carb diet benefits",
    "fat burning zone explained",
    "weight loss without exercise",
    "hunger vs cravings difference",
    "water weight vs fat loss",
    "cortisol and weight gain",
    "sleep and weight loss connection",
    "stress eating solutions",
    "mindful eating benefits",
    "food journal for weight loss",
    "weight loss supplements truth",
    "belly fat burning exercises",
    "visceral fat dangers",
    "subcutaneous fat explained",
    "body recomposition guide",
    "reverse dieting explained",
    "metabolic adaptation truth",
    "set point theory explained",
    "weight loss myths debunked",
    "sustainable weight loss tips",
    "yo yo dieting dangers",
    "weight maintenance strategies",
    "body fat percentage guide",
    "BMI vs body fat",
    "weight loss motivation tips",
    
    # Fitness & Exercise (50 topics)
    "7 minute workout at home",
    "plank challenge 30 days",
    "push ups every day results",
    "squats for bigger glutes",
    "cardio vs weight training",
    "burpees benefits explained",
    "pull ups progression guide",
    "deadlift form tutorial",
    "bench press technique",
    "overhead press benefits",
    "lunges for leg strength",
    "mountain climbers exercise",
    "jumping jacks benefits",
    "box jumps tutorial",
    "kettlebell swing benefits",
    "battle ropes workout",
    "resistance bands exercises",
    "bodyweight training benefits",
    "calisthenics for beginners",
    "CrossFit explained",
    "functional training benefits",
    "compound vs isolation exercises",
    "progressive overload explained",
    "muscle confusion myth",
    "rest days importance",
    "active recovery benefits",
    "stretching before workout",
    "warm up routine importance",
    "cool down exercises",
    "foam rolling benefits",
    "mobility vs flexibility",
    "dynamic stretching guide",
    "static stretching benefits",
    "muscle soreness explained",
    "DOMS recovery tips",
    "overtraining symptoms",
    "deload week benefits",
    "training frequency guide",
    "workout split explained",
    "full body vs split routine",
    "morning vs evening workout",
    "fasted cardio benefits",
    "LISS vs HIIT cardio",
    "steady state cardio benefits",
    "interval training explained",
    "Tabata workout guide",
    "circuit training benefits",
    "superset training explained",
    "drop sets technique",
    "pyramid sets explained",
    
    # Sleep & Recovery (30 topics)
    "sleeping on left side benefits",
    "best sleeping position for health",
    "how to fall asleep in 2 minutes",
    "power nap benefits",
    "sleep and weight loss connection",
    "sleep cycle explained",
    "REM sleep importance",
    "deep sleep benefits",
    "sleep deprivation effects",
    "insomnia natural remedies",
    "sleep apnea symptoms",
    "snoring solutions",
    "sleep hygiene tips",
    "bedroom temperature for sleep",
    "blue light and sleep",
    "melatonin supplement guide",
    "sleep tracking benefits",
    "polyphasic sleep explained",
    "biphasic sleep pattern",
    "sleep debt recovery",
    "napping benefits and risks",
    "sleep paralysis explained",
    "lucid dreaming guide",
    "sleep meditation technique",
    "white noise for sleep",
    "sleep mask benefits",
    "weighted blanket benefits",
    "sleep supplements guide",
    "magnesium for sleep",
    "chamomile tea benefits",
    
    # Nutrition & Diet (50 topics)
    "eating eggs daily benefits",
    "banana before workout benefits",
    "protein intake for muscle gain",
    "best foods for brain health",
    "anti inflammatory foods",
    "superfoods list explained",
    "omega 3 fatty acids benefits",
    "fiber rich foods benefits",
    "complex carbs vs simple carbs",
    "good fats vs bad fats",
    "saturated fat truth",
    "trans fats dangers",
    "cholesterol myths debunked",
    "sodium intake guidelines",
    "sugar addiction explained",
    "artificial sweeteners truth",
    "natural sweeteners guide",
    "stevia vs sugar",
    "honey benefits explained",
    "coconut oil benefits",
    "olive oil health benefits",
    "avocado nutrition facts",
    "nuts for heart health",
    "seeds nutrition benefits",
    "quinoa protein benefits",
    "oats for weight loss",
    "brown rice vs white rice",
    "whole wheat vs refined",
    "gluten free diet explained",
    "dairy free alternatives",
    "plant based protein sources",
    "vegan diet benefits",
    "vegetarian diet guide",
    "pescatarian diet explained",
    "Mediterranean diet benefits",
    "DASH diet explained",
    "paleo diet guide",
    "whole 30 diet explained",
    "flexitarian diet benefits",
    "intuitive eating guide",
    "macro counting explained",
    "micronutrients importance",
    "vitamin deficiency symptoms",
    "mineral deficiency signs",
    "food combining myths",
    "eating frequency myths",
    "breakfast importance debate",
    "late night eating effects",
    "meal timing for athletes",
    "pre workout nutrition",
    
    # Skin & Beauty (30 topics)
    "ice cube facial benefits",
    "aloe vera for glowing skin",
    "vitamin C serum benefits",
    "collagen for anti aging",
    "natural remedies for acne",
    "retinol benefits explained",
    "hyaluronic acid for skin",
    "niacinamide benefits",
    "sunscreen importance daily",
    "double cleansing method",
    "exfoliation benefits",
    "chemical vs physical exfoliant",
    "face masks benefits",
    "sheet masks explained",
    "facial massage benefits",
    "gua sha technique",
    "jade roller benefits",
    "skin care routine order",
    "morning skin care routine",
    "night skin care routine",
    "skin types explained",
    "oily skin care tips",
    "dry skin remedies",
    "combination skin care",
    "sensitive skin solutions",
    "anti aging skin care",
    "dark circles remedies",
    "puffy eyes solutions",
    "skin purging explained",
    "skin barrier repair",
    
    # Mental Health (40 topics)
    "morning routine for success",
    "gratitude journal benefits",
    "digital detox challenge",
    "mindfulness meditation guide",
    "positive affirmations power",
    "anxiety relief techniques",
    "stress management tips",
    "depression warning signs",
    "mental health awareness",
    "self care routine ideas",
    "work life balance tips",
    "burnout prevention strategies",
    "emotional intelligence guide",
    "cognitive behavioral therapy",
    "growth mindset explained",
    "fixed mindset dangers",
    "limiting beliefs removal",
    "self confidence building",
    "self esteem improvement",
    "imposter syndrome solutions",
    "perfectionism dangers",
    "procrastination solutions",
    "time management tips",
    "productivity hacks",
    "focus improvement techniques",
    "concentration exercises",
    "memory improvement tips",
    "brain training exercises",
    "neuroplasticity explained",
    "dopamine detox benefits",
    "social media detox",
    "phone addiction solutions",
    "screen time reduction",
    "nature therapy benefits",
    "forest bathing explained",
    "grounding techniques",
    "breathwork for anxiety",
    "box breathing technique",
    "4 7 8 breathing method",
    "wim hof breathing",
    
    # Immunity & Health (40 topics)
    "boost immunity naturally",
    "vitamin D deficiency symptoms",
    "turmeric milk benefits",
    "ginger tea for cold",
    "probiotics for gut health",
    "immune system explained",
    "white blood cells function",
    "lymphatic system health",
    "inflammation causes",
    "chronic inflammation dangers",
    "autoimmune disease explained",
    "gut health importance",
    "microbiome benefits",
    "fermented foods benefits",
    "kombucha health benefits",
    "kefir vs yogurt",
    "bone broth benefits",
    "collagen supplements guide",
    "elderberry for immunity",
    "echinacea benefits",
    "zinc for immune system",
    "vitamin C megadose",
    "antioxidants explained",
    "free radicals damage",
    "oxidative stress explained",
    "detox myths debunked",
    "liver detox naturally",
    "kidney health tips",
    "lymphatic drainage massage",
    "dry brushing benefits",
    "sauna health benefits",
    "cold plunge benefits",
    "contrast therapy explained",
    "ice bath benefits",
    "heat therapy benefits",
    "infrared sauna benefits",
    "steam room benefits",
    "epsom salt bath benefits",
    "magnesium bath benefits",
    "essential oils benefits",
    
    # Posture & Pain (30 topics)
    "fix forward head posture",
    "desk exercises for office workers",
    "stretches for lower back pain",
    "neck pain relief exercises",
    "improve posture in 30 days",
    "text neck syndrome",
    "computer posture tips",
    "standing desk benefits",
    "ergonomic setup guide",
    "sitting posture correct",
    "sleeping posture guide",
    "shoulder pain relief",
    "rotator cuff exercises",
    "frozen shoulder treatment",
    "tennis elbow relief",
    "carpal tunnel prevention",
    "wrist pain exercises",
    "hip flexor stretches",
    "tight hips solutions",
    "sciatica pain relief",
    "piriformis syndrome",
    "IT band stretches",
    "knee pain relief",
    "ankle mobility exercises",
    "plantar fasciitis relief",
    "flat feet exercises",
    "bunion pain relief",
    "TMJ pain relief",
    "jaw tension release",
    "headache relief pressure points",
    
    # Energy & Vitality (30 topics)
    "natural energy boosters",
    "coffee vs green tea",
    "foods that fight fatigue",
    "morning stretches for energy",
    "cold shower benefits",
    "caffeine tolerance explained",
    "coffee nap technique",
    "matcha green tea benefits",
    "yerba mate benefits",
    "guarana energy benefits",
    "B vitamins for energy",
    "iron deficiency fatigue",
    "thyroid and energy",
    "adrenal fatigue explained",
    "chronic fatigue syndrome",
    "mitochondria and energy",
    "ATP production explained",
    "cellular energy boost",
    "coenzyme Q10 benefits",
    "creatine for energy",
    "beetroot juice benefits",
    "nitric oxide benefits",
    "blood flow improvement",
    "circulation boosting foods",
    "oxygen levels optimization",
    "breathing for energy",
    "energizing yoga poses",
    "morning workout benefits",
    "exercise for energy",
    "movement breaks importance",
    
    # Trending Challenges (30 topics)
    "75 hard challenge explained",
    "no phone before bed challenge",
    "sugar free diet 30 days",
    "daily walking challenge",
    "water fasting benefits",
    "dry january benefits",
    "veganuary challenge",
    "whole 30 challenge",
    "couch to 5k program",
    "100 push ups challenge",
    "30 day plank challenge",
    "squat challenge results",
    "burpee challenge benefits",
    "pull up progression",
    "handstand challenge",
    "splits challenge guide",
    "flexibility challenge",
    "mobility challenge",
    "cold shower challenge",
    "wim hof method",
    "breathwork challenge",
    "meditation streak",
    "gratitude challenge",
    "journaling challenge",
    "reading challenge benefits",
    "no social media challenge",
    "dopamine detox challenge",
    "minimalism challenge",
    "declutter challenge",
    "financial wellness challenge",
    
    # Hormones & Balance (30 topics)
    "hormone balance naturally",
    "cortisol stress hormone",
    "insulin resistance explained",
    "blood sugar balance",
    "testosterone boosting foods",
    "estrogen dominance symptoms",
    "progesterone benefits",
    "thyroid function optimization",
    "growth hormone benefits",
    "melatonin production",
    "serotonin boosting foods",
    "dopamine regulation",
    "endorphins natural high",
    "oxytocin love hormone",
    "adrenaline rush explained",
    "leptin hormone explained",
    "ghrelin hunger hormone",
    "insulin sensitivity",
    "metabolic syndrome",
    "PCOS natural treatment",
    "endometriosis diet",
    "menopause symptoms relief",
    "perimenopause explained",
    "PMS relief naturally",
    "menstrual cycle phases",
    "cycle syncing explained",
    "seed cycling benefits",
    "hormone testing guide",
    "adrenal support naturally",
    "stress hormone reduction",
    
    # Longevity & Anti-Aging (30 topics)
    "blue zones secrets",
    "longevity diet explained",
    "anti aging foods",
    "telomeres and aging",
    "autophagy benefits",
    "fasting for longevity",
    "calorie restriction benefits",
    "sirtuins activation",
    "NAD+ boosting naturally",
    "resveratrol benefits",
    "NMN supplement explained",
    "metformin for longevity",
    "rapamycin anti aging",
    "senolytics explained",
    "cellular senescence",
    "oxidative stress aging",
    "glycation and aging",
    "AGEs in food",
    "collagen production",
    "elastin for skin",
    "bone density maintenance",
    "muscle mass preservation",
    "sarcopenia prevention",
    "brain aging prevention",
    "cognitive decline prevention",
    "Alzheimer prevention diet",
    "dementia risk reduction",
    "neurogenesis promotion",
    "BDNF boosting naturally",
    "longevity supplements guide",
    
    # Muscle Building (40 topics)
    "muscle building for beginners",
    "protein timing for gains",
    "best exercises for chest",
    "back workout routine",
    "shoulder exercises guide",
    "arm workout for mass",
    "leg day importance",
    "glute activation exercises",
    "calf raises benefits",
    "forearm training",
    "grip strength exercises",
    "core strengthening",
    "abs workout routine",
    "six pack abs diet",
    "obliques exercises",
    "lower abs workout",
    "upper abs exercises",
    "transverse abdominis",
    "muscle hypertrophy explained",
    "strength vs size training",
    "power training benefits",
    "explosive strength",
    "isometric exercises",
    "eccentric training",
    "concentric movement",
    "time under tension",
    "mind muscle connection",
    "muscle activation",
    "muscle fiber types",
    "fast twitch vs slow twitch",
    "muscle protein synthesis",
    "anabolic window myth",
    "post workout nutrition",
    "pre workout supplements",
    "creatine monohydrate",
    "beta alanine benefits",
    "citrulline malate",
    "BCAAs explained",
    "EAAs vs BCAAs",
    "whey protein benefits",
    
    # Heart Health (30 topics)
    "cardiovascular health tips",
    "heart rate zones",
    "resting heart rate",
    "heart rate variability",
    "blood pressure naturally",
    "cholesterol management",
    "HDL vs LDL cholesterol",
    "triglycerides explained",
    "heart disease prevention",
    "atherosclerosis explained",
    "coronary artery disease",
    "heart attack warning signs",
    "stroke prevention tips",
    "blood clot prevention",
    "varicose veins treatment",
    "circulation improvement",
    "nitric oxide for heart",
    "omega 3 for heart",
    "fish oil benefits",
    "CoQ10 for heart health",
    "magnesium for heart",
    "potassium benefits",
    "sodium and blood pressure",
    "DASH diet for heart",
    "Mediterranean diet heart",
    "plant based heart health",
    "exercise for heart",
    "cardio benefits explained",
    "aerobic exercise guide",
    "heart rate training",
    
    # Digestion & Gut (30 topics)
    "gut health optimization",
    "digestive enzymes benefits",
    "stomach acid importance",
    "bloating relief tips",
    "gas relief naturally",
    "constipation remedies",
    "diarrhea causes",
    "IBS management tips",
    "SIBO explained",
    "leaky gut syndrome",
    "gut brain connection",
    "vagus nerve stimulation",
    "prebiotics vs probiotics",
    "fiber for digestion",
    "soluble vs insoluble fiber",
    "resistant starch benefits",
    "food intolerances",
    "lactose intolerance",
    "gluten sensitivity",
    "FODMAP diet explained",
    "elimination diet guide",
    "food allergy vs intolerance",
    "histamine intolerance",
    "acid reflux relief",
    "GERD natural treatment",
    "heartburn remedies",
    "ulcer healing naturally",
    "H pylori treatment",
    "digestive bitters benefits",
    "apple cider vinegar digestion",
    
    # Flexibility & Mobility (30 topics)
    "flexibility training guide",
    "mobility exercises daily",
    "hip mobility routine",
    "ankle mobility exercises",
    "shoulder mobility",
    "thoracic spine mobility",
    "wrist mobility exercises",
    "hamstring stretches",
    "quad stretches benefits",
    "calf stretches guide",
    "hip flexor stretches",
    "glute stretches",
    "piriformis stretch",
    "IT band release",
    "foam rolling guide",
    "lacrosse ball massage",
    "trigger point therapy",
    "myofascial release",
    "PNF stretching",
    "ballistic stretching",
    "active stretching",
    "passive stretching",
    "isometric stretching",
    "contract relax stretching",
    "splits training guide",
    "backbend progression",
    "forward fold benefits",
    "spinal twist benefits",
    "cat cow stretch",
    "child pose benefits",
    
    # Performance & Athletics (30 topics)
    "athletic performance tips",
    "speed training guide",
    "agility drills",
    "plyometric exercises",
    "power development",
    "vertical jump training",
    "sprint training benefits",
    "endurance training guide",
    "VO2 max explained",
    "lactate threshold",
    "aerobic capacity",
    "anaerobic training",
    "sports nutrition guide",
    "hydration for athletes",
    "electrolyte balance",
    "carb loading explained",
    "glycogen storage",
    "muscle glycogen",
    "recovery nutrition",
    "protein for recovery",
    "sleep for athletes",
    "overtraining prevention",
    "periodization training",
    "deload week athletes",
    "taper before competition",
    "mental training athletes",
    "visualization technique",
    "sports psychology",
    "performance anxiety",
    "competition preparation",
    
    # Women's Health (30 topics)
    "PCOS diet guide",
    "endometriosis natural relief",
    "menstrual cramps relief",
    "period pain remedies",
    "heavy periods causes",
    "irregular periods solutions",
    "fertility boosting foods",
    "pregnancy nutrition guide",
    "postpartum recovery",
    "breastfeeding nutrition",
    "menopause relief naturally",
    "hot flashes remedies",
    "bone health for women",
    "osteoporosis prevention",
    "iron deficiency women",
    "anemia symptoms",
    "thyroid issues women",
    "hormonal acne treatment",
    "hair loss women causes",
    "prenatal vitamins guide",
    "folate vs folic acid",
    "calcium for women",
    "vitamin D for women",
    "magnesium for PMS",
    "evening primrose oil",
    "vitex for hormones",
    "maca root benefits",
    "ashwagandha for women",
    "adaptogenic herbs",
    "stress and fertility",
    
    # Men's Health (20 topics)
    "testosterone boosting naturally",
    "low testosterone symptoms",
    "muscle building for men",
    "prostate health tips",
    "male fertility improvement",
    "sperm count increase",
    "erectile dysfunction natural",
    "libido boosting foods",
    "zinc for men",
    "vitamin D testosterone",
    "strength training benefits",
    "protein needs for men",
    "creatine for men",
    "hair loss prevention men",
    "beard growth tips",
    "male pattern baldness",
    "finasteride explained",
    "minoxidil benefits",
    "DHT blocker foods",
    "men's mental health",
]


def populate_spreadsheet():
    """Populate Google Sheets with health/fitness topics."""
    print("=" * 80)
    print("POPULATE GOOGLE SHEETS WITH TOPICS")
    print("=" * 80)
    print()
    
    # Get credentials from environment
    credentials_path = os.getenv('GOOGLE_SHEETS_CREDENTIALS')
    spreadsheet_id = os.getenv('GOOGLE_SHEETS_ID')
    
    if not credentials_path:
        print("✗ Error: GOOGLE_SHEETS_CREDENTIALS not set in .env file")
        return False
    
    if not spreadsheet_id:
        print("✗ Error: GOOGLE_SHEETS_ID not set in .env file")
        return False
    
    if not os.path.exists(credentials_path):
        print(f"✗ Error: Credentials file not found: {credentials_path}")
        return False
    
    print(f"✓ Credentials file: {credentials_path}")
    print(f"✓ Spreadsheet ID: {spreadsheet_id}")
    print()
    
    try:
        # Authenticate with Google Sheets
        print("Authenticating with Google Sheets...")
        creds = Credentials.from_service_account_file(
            credentials_path,
            scopes=['https://www.googleapis.com/auth/spreadsheets']
        )
        service = build('sheets', 'v4', credentials=creds)
        print("✓ Authentication successful")
        print()
        
        # Prepare data for spreadsheet
        # Format: [Topic, Duration, Status, Video URL]
        print(f"Preparing {len(HEALTH_FITNESS_TOPICS)} topics...")
        
        # Header row
        values = [
            ['Topic', 'Duration (seconds)', 'Status', 'Video URL']
        ]
        
        # Add all topics with 20 second duration
        for topic in HEALTH_FITNESS_TOPICS:
            values.append([
                topic,
                20,  # 20 seconds duration
                'pending',  # Status
                ''  # Video URL (empty initially)
            ])
        
        print(f"✓ Prepared {len(HEALTH_FITNESS_TOPICS)} topics")
        print()
        
        # Ask user for confirmation
        print("This will:")
        print(f"  1. Clear existing data in the 'Videos' sheet")
        print(f"  2. Add {len(HEALTH_FITNESS_TOPICS)} new topics")
        print()
        
        response = input("Continue? (yes/no): ").strip().lower()
        
        if response not in ['yes', 'y']:
            print("Cancelled.")
            return False
        
        print()
        print("Writing to Google Sheets...")
        
        # Clear existing data first
        sheet_name = 'Videos'
        range_name = f'{sheet_name}!A1:D1000'
        
        service.spreadsheets().values().clear(
            spreadsheetId=spreadsheet_id,
            range=range_name
        ).execute()
        
        print("✓ Cleared existing data")
        
        # Write new data
        body = {
            'values': values
        }
        
        result = service.spreadsheets().values().update(
            spreadsheetId=spreadsheet_id,
            range=f'{sheet_name}!A1',
            valueInputOption='RAW',
            body=body
        ).execute()
        
        updated_cells = result.get('updatedCells', 0)
        
        print(f"✓ Successfully wrote {updated_cells} cells")
        print(f"✓ Added {len(HEALTH_FITNESS_TOPICS)} topics to spreadsheet")
        print()
        
        # Show spreadsheet URL
        spreadsheet_url = f"https://docs.google.com/spreadsheets/d/{spreadsheet_id}"
        print("=" * 80)
        print("SUCCESS!")
        print("=" * 80)
        print()
        print(f"View your spreadsheet:")
        print(f"{spreadsheet_url}")
        print()
        print("Topics added:")
        for i, topic in enumerate(HEALTH_FITNESS_TOPICS[:10], 1):
            print(f"  {i}. {topic}")
        print(f"  ... and {len(HEALTH_FITNESS_TOPICS) - 10} more!")
        print()
        
        return True
        
    except HttpError as e:
        print(f"✗ Google Sheets API error: {e}")
        return False
    except Exception as e:
        print(f"✗ Error: {e}")
        return False


if __name__ == "__main__":
    print()
    
    # Load environment variables
    from dotenv import load_dotenv
    load_dotenv()
    
    success = populate_spreadsheet()
    
    if success:
        print("=" * 80)
        print("NEXT STEPS:")
        print("=" * 80)
        print()
        print("1. Open your Google Sheets spreadsheet")
        print("2. Review the topics")
        print("3. Edit/add/remove topics as needed")
        print("4. Run the automation:")
        print("   python automation_scheduler.py")
        print()
    else:
        print()
        print("Setup failed. Please check the errors above.")
        print()

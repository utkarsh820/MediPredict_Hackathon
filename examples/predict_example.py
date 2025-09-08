import os
import sys
import json

# Add project root to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src import predict_from_symptoms, get_all_symptoms

def main():
    # Sample symptoms input
    symptoms = {
        "itching": 1,
        "skin_rash": 1,
        "nodal_skin_eruptions": 1,
        "dischromic_patches": 0
    }
    
    # Get prediction
    print("Making prediction...")
    result = predict_from_symptoms(symptoms, model_type='xgb')
    
    # Print results
    print(f"\nPredicted Disease: {result['prediction']}")
    print(f"Confidence: {result['confidence']:.4f}")
    print(f"Model Used: {result['model']}")
    
    # Print related symptoms
    print("\nRelated Symptoms:")
    for symptom in result['related_symptoms']:
        print(f"- {symptom['symptom']} ({symptom['count']} occurrences)")
    
    # Print available symptoms
    print("\nAvailable Symptoms (first 10):")
    all_symptoms = get_all_symptoms()
    for symptom in all_symptoms[:10]:
        print(f"- {symptom}")
    print(f"... and {len(all_symptoms) - 10} more")

if __name__ == "__main__":
    main()

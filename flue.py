def check_patient(patient):
    name = str(patient.get("name", "")).strip()
    temperature = patient.get("temperature")
    saturation = patient.get("saturation")

    if not name:
        return {
            "message": "Please enter patient's name",
            "status": "error"
        }

    if temperature is None or temperature == "":
        return {
            "message": f"{name}: Temperature is required",
            "status": "error"
        }

    if saturation is None or saturation == "":
        return {
            "message": f"{name}: Saturation is required",
            "status": "error"
        }

    try:
        temperature = float(str(temperature).replace(",", "."))
    except (ValueError, TypeError):
        return {
            "message": f"{name}: Invalid temperature value",
            "status": "error"
        }

    try:
        saturation = int(saturation)
    except (ValueError, TypeError):
        return {
            "message": f"{name}: Invalid saturation value",
            "status": "error"
        }

    if not 0 <= saturation <= 100:
        return {
            "message": f"{name}: Invalid saturation value",
            "status": "error"
        }

    if not 35 <= temperature <= 45:
        return {
            "message": f"{name}: Invalid temperature value",
            "status": "error"
        }

    patients_diagnoses = [
        (
            lambda t, s: t >= 39 and s <= 92,
            "High risk condition! High fever and low saturation",
            "high"
        ),
        (
            lambda t, s: t >= 38 and s <= 94,
            "Increased risk. Fever and reduced saturation detected",
            "mid"
        ),
        (
            lambda t, s: t >= 38,
            "Fever detected",
            "low"
        ),
        (
            lambda t, s: s <= 94,
            "Reduced saturation detected",
            "low"
        )
    ]

    for condition, diagnosis, status in patients_diagnoses:
        if condition(temperature, saturation):
            return {
                "message": f"{name}: {diagnosis}",
                "status": status
            }

    return {
        "message": f"{name}: Condition is within normal limits",
        "status": "ok"
    }

# CLassic code:
# def input_patient(patient_number):
#     print(f"\n Patient {patient_number} ")

#     name = input("Enter the patient name: ").strip()
#     temperature = float(input("Enter temperature in degrees by Celcium: ").replace(",", "."))
#     saturation_oxygen = int(input("Enter saturation (in %): "))

#     return {
#         "name": name,
#         "temperature": temperature,
#         "saturation": saturation_oxygen
#     }

#     #return patient

# def check_patient(patient):
#     name = patient["name"]
#     temperature = patient["temperature"]
#     saturation = patient["saturation"]

#     #here we start adding the "rules" of the program

#     if not name:
#         return "Please enter patient's name"
#     if not 0 <= saturation <= 100:
#         return f"{name}: Invalid saturation value"
#     if not 30 <= temperature <= 45:
#         return f"{name}: Invalid temperature value"
#     #checking is all of the data is valid

#     patients_diagnoses = [
#         (
#             lambda t, s: t >= 39 and s <= 92,
#             "High risk condition! High fever and low saturation"
#         ),
#         (
#             lambda t, s: t >= 38 and s <= 94,
#             "Increased risk. Fever and reduced saturation detected"
#         ),
#         (
#             lambda t, s: t >= 38,
#             "Fever detected"
#         ),
#         (
#             lambda t, s: s <= 94,
#             "Reduced saturation detected"
#         )
#     ]

#     for condition_ofpatient, diagnose in patients_diagnoses:
#         if condition_ofpatient(temperature, saturation):
#             return f"{name}: {diagnose}"
#     return f"{name}: Condition is within normal limits" #if everything is OK!

# def main():
#     patients = [] #our patients are here

#     count = int(input("Enter number of patients: "))
#     for i in range(1, count + 1):
#         patients.append(input_patient(i))

#     print("\nResults:")
#     for patient in patients:
#         print(check_patient(patient))

# if __name__ == "__main__":
#     main()

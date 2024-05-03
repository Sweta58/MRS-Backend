from django.conf import settings

def clean(ocrResult):
    try:
        minConfidence = 25.00
        goodTexts = []
        for i in range(len(ocrResult)):
            confidence = format(ocrResult[i][2]*100, '.2f')
            if (len(ocrResult[i][1]) > 3) and (float(confidence) > minConfidence):
                goodTexts.append(ocrResult[i][1].lower())
        return goodTexts
    except Exception as e:
        with open('MRS/logs/activities.txt', 'a') as file:
            file.write(f'An exception occurred in clean(ocrResult) function.\n{e}\n')

def identifyMedicines(text):
    try:
        names = []
        for sentence in text:
            fuzzyResult = lookup(sentence)
            names.append(fuzzyResult)
        
        result = [item for item in names if item != '']
        with open('MRS/logs/activities.txt', 'a') as file:
            file.write(f"Medicines Identified = {result}\n") 
        return result
    except Exception as e:
        with open('MRS/logs/activities.txt', 'a') as file:
            file.write(f'An exception occurred in identifyMedicines(text) function.\n{e}\n')

def lookup(query):
    try:
        import os
        from django.conf import settings
        ndcPath = os.path.join(settings.BASE_DIR, 'MRS', 'dataset', 'generic_names.txt')
        from thefuzz import fuzz

        match = ''
        matchRatio = 0
        with open(ndcPath, "r") as data:
            for line in data:
                similarity = fuzz.ratio(query, line.rstrip())
                if similarity > 85 and similarity > matchRatio:
                    matchRatio = similarity
                    match = line.rstrip()
        with open('MRS/logs/activities.txt', 'a') as file:
            file.write(f"{query} = <<{match}>>\n")           
        return match
    except Exception as e:
        with open('MRS/logs/activities.txt', 'a') as file:
            file.write(f'An exception occurred in lookup(query) function.\n{e}\n')
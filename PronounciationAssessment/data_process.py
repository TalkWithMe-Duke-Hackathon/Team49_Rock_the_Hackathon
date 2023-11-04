import json
import csv

index = 0;

data = '''{
  "RecognitionStatus": "Success",
  "Offset": 900000,
  "Duration": 18800000,
  "NBest": [
    {
      "Lexical": "hi how are you",
      "ITN": "hi how are you",
      "MaskedITN": "hi how are you",
      "Display": "Hi, how are you?",
      "AccuracyScore": 98.0,
      "FluencyScore": 100.0,
      "CompletenessScore": 100.0,
      "PronScore": 98.8,
      "Words": [
        {
          "Word": "hi",
          "AccuracyScore": 92.0,
          "ErrorType": "None",
          "Offset": 3800000,
          "Duration": 4200000,
          "Syllables": [
            {
              "Syllable": "hay",
              "AccuracyScore": 76.0,
              "Offset": 3800000,
              "Duration": 4200000
            }
          ],
          "Phonemes": [
            {
              "Phoneme": "h",
              "AccuracyScore": 69.0,
              "Offset": 3800000,
              "Duration": 2800000
            },
            {
              "Phoneme": "ay",
              "AccuracyScore": 89.0,
              "Offset": 6700000,
              "Duration": 1300000
            }
          ]
        },
        {
          "Word": "how",
          "AccuracyScore": 100.0,
          "ErrorType": "None",
          "Offset": 8100000,
          "Duration": 1600000,
          "Syllables": [
            {
              "Syllable": "haw",
              "AccuracyScore": 100.0,
              "Offset": 8100000,
              "Duration": 1600000
            }
          ],
          "Phonemes": [
            {
              "Phoneme": "h",
              "AccuracyScore": 100.0,
              "Offset": 8100000,
              "Duration": 1300000
            },
            {
              "Phoneme": "aw",
              "AccuracyScore": 100.0,
              "Offset": 9500000,
              "Duration": 200000
            }
          ]
        },
        {
          "Word": "are",
          "AccuracyScore": 100.0,
          "ErrorType": "None",
          "Offset": 9800000,
          "Duration": 3200000,
          "Syllables": [
            {
              "Syllable": "aar",
              "AccuracyScore": 100.0,
              "Offset": 9800000,
              "Duration": 3200000
            }
          ],
          "Phonemes": [
            {
              "Phoneme": "aa",
              "AccuracyScore": 100.0,
              "Offset": 9800000,
              "Duration": 1400000
            },
            {
              "Phoneme": "r",
              "AccuracyScore": 100.0,
              "Offset": 11300000,
              "Duration": 1700000
            }
          ]
        },
        {
          "Word": "you",
          "AccuracyScore": 100.0,
          "ErrorType": "None",
          "Offset": 13100000,
          "Duration": 5300000,
          "Syllables": [
            {
              "Syllable": "yuw",
              "AccuracyScore": 100.0,
              "Offset": 13100000,
              "Duration": 5300000
            }
          ],
          "Phonemes": [
            {
              "Phoneme": "y",
              "AccuracyScore": 100.0,
              "Offset": 13100000,
              "Duration": 1300000
            },
            {
              "Phoneme": "uw",
              "AccuracyScore": 100.0,
              "Offset": 14500000,
              "Duration": 3900000
            }
          ]
        }
      ]
    }
  ]
}'''

# Parse the JSON data
data_dict = json.loads(data)

# Extract the values
accuracy_score = data_dict["NBest"][0]["AccuracyScore"]
fluency_score = data_dict["NBest"][0]["FluencyScore"]
completeness_score = data_dict["NBest"][0]["CompletenessScore"]
pron_score = data_dict["NBest"][0]["PronScore"]

# Write the scores to a CSV file
with open('scores.csv', 'w', newline='') as csvfile:
    fieldnames = ['Index','AccuracyScore','FluencyScore','CompletenessScor','PronScore']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    writer.writeheader()
    writer.writerow({'Index': index, 'AccuracyScore': accuracy_score, 'FluencyScore' : fluency_score, 'CompletenessScor':completeness_score, 'PronScore':pron_score})
    index += 1
from google_Distance import getDistance
from google_Stores import getStores
from google_Score import getScore

print(getDistance('ARIUM Westside, 1000 Northside Dr NW, Atlanta, GA 30318', '255 Courtland St NE, Atlanta, GA 30303'))

print("\n")

print(getStores('ARIUM Westside, 1000 Northside Dr NW, Atlanta, GA 30318','food'))

print("\n")

print(getScore('ARIUM Westside, 1000 Northside Dr NW, Atlanta, GA 30318'))

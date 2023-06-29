# Advanced Queries

## Advanced Query 1:
Finding names of dining halls that offer at least one of the same meals - we can use this to compare similar dining options in the final app.

```
SELECT h.Name
FROM DiningHall h NATURAL JOIN Menu NATURAL JOIN Meal WHERE MealID IN (
  SELECT MealID FROM DiningHall NATURAL JOIN Menu NATURAL JOIN Meal
  GROUP BY MealID HAVING count(*) > 1)

LIMIT 15
```
![image](https://user-images.githubusercontent.com/20449375/197293201-3870b094-d0d0-4f2b-b0f9-90d762ac5604.png)


## Advanced Query 2:
Listing restrictions that apply to at least one student - we can use this to list the most common restrictions for students.
```
USE dining;

SELECT r.RestrictionID
FROM Student s NATURAL JOIN Restriction r 
GROUP BY r.RestrictionID
HAVING COUNT(s.StudentID) > 1

LIMIT 15
```
<img width="282" alt="image" src="https://user-images.githubusercontent.com/20449375/197292850-37a30437-b33b-41ce-a21a-6ff3ed2d8405.png">

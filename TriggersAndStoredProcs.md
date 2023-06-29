**TRIGGER 1 CODE**

USE dining ;

DELIMITER //

CREATE TRIGGER DeleteAllStudents

AFTER DELETE ON Student 

FOR EACH ROW 

BEGIN 

    SET @totalStudents = (SELECT COUNT(*) FROM Student s WHERE s.Restrictions = OLD.Restrictions);
	
    IF @totalStudents = 0 THEN
    
		UPDATE Restriction SET Restriction.Status = "Inactive" WHERE Restriction.RestrictionID = OLD.Restrictions;
		
    END IF; 
    
END; //

DELIMITER ;

**TRIGGER 2 CODE**

USE dining ;

DELIMITER //

CREATE TRIGGER InsertNewStudents

AFTER INSERT ON Student 

FOR EACH ROW 

BEGIN 

    SET @totalStudents = (SELECT COUNT(*) FROM Student s WHERE s.Restrictions = NEW.Restrictions);
	
    IF @totalStudents = 1 THEN
    
		UPDATE Restriction SET Restriction.Status = "Active" WHERE Restriction.RestrictionID = NEW.Restrictions;
		
    END IF; 
    
END; //

DELIMITER ;


**PROCEDURE CODE**

use dining;

DELIMITER //

CREATE PROCEDURE checkForRemovable (IN InMealID VARCHAR(225), OUT Removable BOOLEAN, OUT StudentsStarved INTEGER) BEGIN

DECLARE currStudent VARCHAR(225);

DECLARE overlapWithSelected INTEGER;

DECLARE done BOOLEAN DEFAULT FALSE;


DECLARE cantEatOthers BOOLEAN DEFAULT FALSE;

DECLARE currMeal VARCHAR(225);

DECLARE doneInner BOOLEAN DEFAULT FALSE;

DECLARE curs CURSOR FOR (SELECT StudentID FROM Student);

DECLARE CONTINUE HANDLER FOR NOT FOUND SET done = TRUE;

SET Removable = FALSE;

SET StudentsStarved = 0;

OPEN curs;

cloop: LOOP 

	FETCH curs INTO currStudent;
	
	IF(done) THEN 
	
        LEAVE cloop;
	
  	END IF;
    
	(SELECT COUNT(DISTINCT MealID) INTO overlapWithSelected
	
	FROM (Student JOIN (Restriction r JOIN Meal m) ON r.Ingredients=m.Ingredients)
	
	WHERE StudentID=currStudent AND MealID=InMealID);

	IF (overlapWithSelected=1) THEN 
	
		SET Removable = FALSE;
		
        	SET StudentsStarved = StudentsStarved+1;
		
    END IF;

END LOOP cloop;

CLOSE curs;

END //

DELIMITER ;

-- Write query to get number of graded assignments for each student:

SELECT student_id, COUNT(*) AS graded_assignments_count
FROM assignments
WHERE grade IS NOT NULL  -- Assuming graded assignments have a non-null grade
GROUP BY student_id
ORDER BY student_id;

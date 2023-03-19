SELECT * FROM sqlpractice1.employee_attrition_train;

#1 write an sql query to find employee 5+ exp &age btwn 27-35

SELECT * 
FROM sqlpractice1.employee_attrition_train
WHERE Age between 27 and 35
and TotalWorkingYears >= 5;
#count values
SELECT count(*) 
FROM sqlpractice1.employee_attrition_train
WHERE Age between 27 and 35
and TotalWorkingYears >= 5;

#2Employees having maximum and minimum salary from diff departmentswho received less than 13% salary hike

select department, max(MonthlyIncome),min(MonthlyIncome) from sqlpractice1.employee_attrition_train
where PercentSalaryHike < 13
group by Department;

# 3 Calculate the average monthly income of all employees who is having more than 3 years of experience and education background is medical
select * -- avg(MonthlyIncome)
from sqlpractice1.employee_attrition_train
where YearsAtCompany > 3 
and EducationField='Medical'
group by EducationField ;


# 4enter the total number of male and female employees whose marrital status is married and havent received promotion in last 2 years

SELECT Gender,Count(EmployeeNumber)
from sqlpractice1.employee_attrition_train
WHERE MaritalStatus ='Married'
and YearsSinceLastPromotion = 2
group by gender;

# 5 EMPLOYEES WITH THE MOST PERFORMANCE RATING BUT NO PROMOTION SINCE THE LAST 4 YEARS

SELECT  * from sqlpractice1.employee_attrition_train
where PerformanceRating=(select max(PerformanceRating) from sqlpractice1.employee_attrition_train)
and YearsSinceLastPromotion >= 4; 

# 6 Who has maximum and minimum salary hike

SELECT YearsAtCompany,PerformanceRating,YearsSinceLastPromotion,
max(PercentSalaryHike),
min(PercentSalaryHike)
from sqlpractice1.employee_attrition_train
group by YearsAtCompany,PerformanceRating,YearsSinceLastPromotion
order by max(PercentSalaryHike) desc, min(PercentSalaryHike) asc;

#7 Display all departments inthe datasets
select distinct Department from sqlpractice1.employee_attrition_train;

#8 EMPLOYEES WORKING OVERTIME BUT GIVEN MIN SALARY AND MORE THAN 5 YERAS AT THE COMPANY
select *
from sqlpractice1.employee_attrition_train
where OverTime ='Yes'
and PercentSalaryHike= (select min(PercentSalaryHike) from sqlpractice1.employee_attrition_train)
and YearsAtCompany > 5;

#9 EMPLOYEES NOT WORKING OVERTIME BUT GIVEN MIN SALARY AND LESS THAN 5 YERAS AT THE COMPANY

select *
from sqlpractice1.employee_attrition_train
where OverTime ='No'
and PercentSalaryHike= (select min(PercentSalaryHike) from sqlpractice1.employee_attrition_train)
and YearsAtCompany < 5;

#10 EMPLOYEES WORKING OVERTIME BUT GIVEN MAX SALARY AND MORE THAN 5 YERAS AT THE COMPANY

select *
from sqlpractice1.employee_attrition_train
where OverTime ='Yes'
and PercentSalaryHike= (select max(PercentSalaryHike) from sqlpractice1.employee_attrition_train)
and YearsAtCompany > 5;

#11 EMPLOYEES NOT WORKING OVERTIME BUT GIVEN MAX SALARY AND LESS THAN 5 YERAS AT THE COMPANY

select *
from sqlpractice1.employee_attrition_train
where OverTime ='No'
and PercentSalaryHike= (select max(PercentSalaryHike) from sqlpractice1.employee_attrition_train)
and YearsAtCompany < 5;
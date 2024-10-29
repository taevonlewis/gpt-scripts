## Title: Custom Calendar View

### Problem Statement:

You are tasked with creating a custom calendar view for an iOS application. The view should display a full month with dates and allow users to select a range of dates. 

You should write a function that will generate the calendar view and enable the user to select a date range. The selected date range should be highlighted with a different color to provide a visual difference. The calendar should also handle situations where the date range spans across multiple months.

Your function should be able to handle the following scenarios:

- The user selects a start date and an end date that are both in the same month.
- The user selects a start date in one month, and an end date in the following month.
- The user selects a start date in one month, and an end date in a month that is not immediately following the start date.

Function Signature: `func createCalendarView(startDate: Date, endDate: Date) -> UIView`

### Constraints:

- The function takes two parameters: `startDate` and `endDate`. Both are instances of `Date` and `startDate` is always less than or equal to `endDate`.
- The function should return a `UIView` that represents the calendar.
- The calendar should be a grid with 7 columns (for the 7 days of the week) and enough rows to accommodate the dates in the given range.
- The calendar should display the full month for the start and end dates.
- If the selected date range spans across multiple months, the calendar should display all the months within the range, each as a separate month grid.
- The dates that fall within the selected range should be highlighted with a different color.

### Examples:

#### Example 1:

If `startDate` is "2022-01-01" and `endDate` is "2022-01-15", the function should return a calendar view for January 2022 with dates 1 to 15 highlighted.

#### Example 2:

If `startDate` is "2022-01-28" and `endDate` is "2022-02-05", the function should return a calendar view for January and February 2022 with dates 28, 29, 30, 31 of January and 1, 2, 3, 4, 5 of February highlighted.

#### Example 3:

If `startDate` is "2022-01-15" and `endDate` is "2022-03-15", the function should return a calendar view for January, February, and March 2022 with dates 15 to 31 of January, all dates of February, and 1 to 15 of March highlighted.

### Optimal Time and Space Complexity:

The time complexity should be O(1) as the number of days in a month is fixed (28 to 31 days). The space complexity should also be O(1) as the size of the UIView does not change with the input size.
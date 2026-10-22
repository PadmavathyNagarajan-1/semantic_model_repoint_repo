CREATE TABLE [dbo].[TimeEntries_Vishnu] (
    [EmployeeID]   INT           IDENTITY (1, 1) NOT NULL,
    [EmployeeName] VARCHAR (255) NULL,
    [Department]   VARCHAR (255) NULL,
    [Project]      VARCHAR (255) NULL,
    [Task]         VARCHAR (255) NULL,
    [Date]         DATE          NULL,
    [HoursWorked]  FLOAT (53)    NULL,
    [Location]     VARCHAR (255) NULL,
    [Manager]      VARCHAR (255) NULL,
    [Billable]     VARCHAR (255) NULL,
    CONSTRAINT [PK_TimeEntries_Vishnu_EmployeeID_e29cb7951e] PRIMARY KEY CLUSTERED ([EmployeeID] ASC)
);


GO


CREATE TABLE [dbo].[employee] (
    [employee_id]       VARCHAR (255)   NOT NULL,
    [first_name]        VARCHAR (255)   NOT NULL,
    [last_name]         VARCHAR (255)   NOT NULL,
    [job_title]         VARCHAR (255)   NOT NULL,
    [department_id]     INT             NOT NULL,
    [start_date]        DATE            NOT NULL,
    [end_date]          DATE            NULL,
    [incentive]         VARCHAR (255)   NULL,
    [target_bonus]      DECIMAL (10, 2) NULL,
    [salary]            INT             NULL,
    [active_employment] INT             NOT NULL,
    CONSTRAINT [PK_employee] PRIMARY KEY CLUSTERED ([employee_id] ASC),
    CONSTRAINT [FK_department] FOREIGN KEY ([department_id]) REFERENCES [dbo].[department] ([department_id])
);


GO


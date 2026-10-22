CREATE TABLE [dbo].[Sheet2] (
    [ID]           INT            NOT NULL,
    [Emoji]        NVARCHAR (255) NULL,
    [Arab]         NVARCHAR (255) NULL,
    [Jappan]       NVARCHAR (255) NULL,
    [Tamil]        NVARCHAR (255) NULL,
    [Empty Column] VARCHAR (255)  NULL,
    [Start_Date]   DATE           NULL,
    [End_Date]     DATE           NULL,
    CONSTRAINT [PK_Sheet2_ID_69826f6a49] PRIMARY KEY CLUSTERED ([ID] ASC)
);


GO


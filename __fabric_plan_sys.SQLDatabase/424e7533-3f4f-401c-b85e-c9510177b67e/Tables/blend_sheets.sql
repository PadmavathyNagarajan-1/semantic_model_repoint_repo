CREATE TABLE [424e7533-3f4f-401c-b85e-c9510177b67e].[blend_sheets] (
    [id]        NVARCHAR (128) NOT NULL,
    [name]      VARCHAR (255)  NOT NULL,
    [type]      INT            NOT NULL,
    [meta]      NVARCHAR (MAX) NOT NULL,
    [createdAt] INT            NOT NULL,
    [updatedAt] INT            NOT NULL,
    [createdBy] NVARCHAR (128) NOT NULL,
    [updatedBy] NVARCHAR (128) NOT NULL,
    CONSTRAINT [PK_blend_sheets] PRIMARY KEY CLUSTERED ([id] ASC)
);


GO


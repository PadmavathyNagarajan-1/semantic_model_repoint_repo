CREATE TABLE [8a1bb6d2-7685-4f22-b230-fc8749890316].[planning_settings_audit] (
    [id]            INT            IDENTITY (1, 1) NOT NULL,
    [entityId]      INT            NULL,
    [entityType]    INT            NOT NULL,
    [visualId]      INT            NOT NULL,
    [value]         NVARCHAR (MAX) NULL,
    [operationType] INT            CONSTRAINT [DF_6cb74b6b827715c7aee56a03aec] DEFAULT ((2)) NOT NULL,
    [measureGuid]   NVARCHAR (255) NULL,
    [updatedBy]     NVARCHAR (128) NOT NULL,
    [updatedByUPN]  NVARCHAR (320) NOT NULL,
    [updatedAt]     INT            NOT NULL,
    CONSTRAINT [PK_ac5a125faf87569831de66f874f] PRIMARY KEY CLUSTERED ([id] ASC)
);


GO

CREATE NONCLUSTERED INDEX [idx_planning_settings_audit_visualId]
    ON [8a1bb6d2-7685-4f22-b230-fc8749890316].[planning_settings_audit]([visualId] ASC);


GO


CREATE TABLE [8a580838-3856-4c02-8df8-2a3c4403df41].[visual_di_4_22fca963e59ef33bb97423e0e1d4cfeb] (
    [id]                     BIGINT           IDENTITY (1, 1) NOT NULL,
    [rowId]                  NVARCHAR (255)   NOT NULL,
    [colId]                  NVARCHAR (255)   NOT NULL,
    [scenarioId]             INT              NULL,
    [filterContextHash]      NVARCHAR (255)   NULL,
    [updatedAt]              INT              NOT NULL,
    [updatedBy]              NVARCHAR (128)   NOT NULL,
    [dim_DimPlantMasterCity] NVARCHAR (255)   NULL,
    [measure_9]              DECIMAL (30, 10) NULL,
    [measure_9_meta]         NVARCHAR (255)   NULL,
    PRIMARY KEY CLUSTERED ([id] ASC),
    UNIQUE NONCLUSTERED ([rowId] ASC, [colId] ASC, [scenarioId] ASC, [filterContextHash] ASC)
);


GO


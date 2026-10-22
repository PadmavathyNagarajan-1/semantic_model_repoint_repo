CREATE TABLE [3e11f521-d002-4710-9f4f-55c488cfd03f].[visual_di_4_22fca963e59ef33bb97423e0e1d4cfeb] (
    [id]                     BIGINT           IDENTITY (1, 1) NOT NULL,
    [rowId]                  NVARCHAR (255)   NOT NULL,
    [colId]                  NVARCHAR (255)   NOT NULL,
    [scenarioId]             INT              NULL,
    [filterContextHash]      NVARCHAR (255)   NULL,
    [updatedAt]              INT              NOT NULL,
    [updatedBy]              NVARCHAR (128)   NOT NULL,
    [dim_DimPlantMasterCity] NVARCHAR (255)   NULL,
    [measure_4]              DECIMAL (30, 10) NULL,
    [measure_4_meta]         NVARCHAR (255)   NULL,
    PRIMARY KEY CLUSTERED ([id] ASC),
    UNIQUE NONCLUSTERED ([rowId] ASC, [colId] ASC, [scenarioId] ASC, [filterContextHash] ASC)
);


GO


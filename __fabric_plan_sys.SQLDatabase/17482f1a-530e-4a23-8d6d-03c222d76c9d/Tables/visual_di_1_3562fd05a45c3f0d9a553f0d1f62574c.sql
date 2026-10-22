CREATE TABLE [17482f1a-530e-4a23-8d6d-03c222d76c9d].[visual_di_1_3562fd05a45c3f0d9a553f0d1f62574c] (
    [id]                                                         BIGINT           IDENTITY (1, 1) NOT NULL,
    [rowId]                                                      NVARCHAR (255)   NOT NULL,
    [colId]                                                      NVARCHAR (255)   NOT NULL,
    [scenarioId]                                                 INT              NULL,
    [filterContextHash]                                          NVARCHAR (255)   NULL,
    [updatedAt]                                                  INT              NOT NULL,
    [updatedBy]                                                  NVARCHAR (128)   NOT NULL,
    [dim_FACT_03_GLAActualCountry]                               NVARCHAR (255)   NULL,
    [dim_FACT_03_GLAActualGLAccount]                             NVARCHAR (255)   NULL,
    [dim_LocalDateTable_68bb40e7925b4d4fa0adf946010b1c74Year]    NVARCHAR (255)   NULL,
    [dim_LocalDateTable_68bb40e7925b4d4fa0adf946010b1c74Quarter] NVARCHAR (255)   NULL,
    [dim_LocalDateTable_68bb40e7925b4d4fa0adf946010b1c74Month]   NVARCHAR (255)   NULL,
    [dim_LocalDateTable_68bb40e7925b4d4fa0adf946010b1c74Day]     NVARCHAR (255)   NULL,
    [measure_1]                                                  DECIMAL (30, 10) NULL,
    [measure_1_meta]                                             NVARCHAR (255)   NULL,
    PRIMARY KEY CLUSTERED ([id] ASC),
    UNIQUE NONCLUSTERED ([rowId] ASC, [colId] ASC, [scenarioId] ASC, [filterContextHash] ASC)
);


GO


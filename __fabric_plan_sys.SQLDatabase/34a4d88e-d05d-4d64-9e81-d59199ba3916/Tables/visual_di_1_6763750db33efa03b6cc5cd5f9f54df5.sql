CREATE TABLE [34a4d88e-d05d-4d64-9e81-d59199ba3916].[visual_di_1_6763750db33efa03b6cc5cd5f9f54df5] (
    [id]                                                         BIGINT           IDENTITY (1, 1) NOT NULL,
    [rowId]                                                      NVARCHAR (255)   NOT NULL,
    [colId]                                                      NVARCHAR (255)   NOT NULL,
    [scenarioId]                                                 INT              NULL,
    [filterContextHash]                                          NVARCHAR (255)   NULL,
    [updatedAt]                                                  INT              NOT NULL,
    [updatedBy]                                                  NVARCHAR (128)   NOT NULL,
    [dim_ListOfOrdersCountry]                                    NVARCHAR (255)   NULL,
    [dim_ListOfOrdersCity]                                       NVARCHAR (255)   NULL,
    [dim_LocalDateTable_3b5613f64ae24443a39fcf4430a9b7d7Year]    NVARCHAR (255)   NULL,
    [dim_LocalDateTable_3b5613f64ae24443a39fcf4430a9b7d7Quarter] NVARCHAR (255)   NULL,
    [dim_LocalDateTable_3b5613f64ae24443a39fcf4430a9b7d7Month]   NVARCHAR (255)   NULL,
    [measure_1]                                                  DECIMAL (30, 10) NULL,
    [measure_2]                                                  DECIMAL (30, 10) NULL,
    [measure_1_meta]                                             NVARCHAR (255)   NULL,
    [measure_2_meta]                                             NVARCHAR (255)   NULL,
    [measure_3]                                                  DECIMAL (30, 10) NULL,
    [measure_3_meta]                                             NVARCHAR (255)   NULL,
    [measure_5]                                                  DECIMAL (30, 10) NULL,
    [measure_5_meta]                                             NVARCHAR (255)   NULL,
    PRIMARY KEY CLUSTERED ([id] ASC),
    UNIQUE NONCLUSTERED ([rowId] ASC, [colId] ASC, [scenarioId] ASC, [filterContextHash] ASC)
);


GO


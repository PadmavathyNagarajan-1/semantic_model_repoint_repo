CREATE TABLE [34a4d88e-d05d-4d64-9e81-d59199ba3916].[visual_audit_1_6763750db33efa03b6cc5cd5f9f54df5] (
    [id]                                                         BIGINT          IDENTITY (1, 1) NOT NULL,
    [rowId]                                                      NVARCHAR (2048) NOT NULL,
    [colId]                                                      NVARCHAR (2048) NOT NULL,
    [scenarioGuid]                                               NVARCHAR (255)  NULL,
    [measureGuid]                                                NVARCHAR (255)  NULL,
    [filterContextHash]                                          NVARCHAR (255)  NULL,
    [action]                                                     NVARCHAR (255)  NULL,
    [meta]                                                       NVARCHAR (MAX)  NULL,
    [oldValue]                                                   NVARCHAR (MAX)  NULL,
    [newValue]                                                   NVARCHAR (MAX)  NULL,
    [updatedAt]                                                  INT             NOT NULL,
    [updatedByUPN]                                               NVARCHAR (320)  NOT NULL,
    [updatedBy]                                                  NVARCHAR (128)  NOT NULL,
    [dim_ListOfOrdersCountry]                                    NVARCHAR (255)  NULL,
    [dim_ListOfOrdersCity]                                       NVARCHAR (255)  NULL,
    [dim_LocalDateTable_3b5613f64ae24443a39fcf4430a9b7d7Year]    NVARCHAR (255)  NULL,
    [dim_LocalDateTable_3b5613f64ae24443a39fcf4430a9b7d7Quarter] NVARCHAR (255)  NULL,
    [dim_LocalDateTable_3b5613f64ae24443a39fcf4430a9b7d7Month]   NVARCHAR (255)  NULL,
    PRIMARY KEY CLUSTERED ([id] ASC)
);


GO


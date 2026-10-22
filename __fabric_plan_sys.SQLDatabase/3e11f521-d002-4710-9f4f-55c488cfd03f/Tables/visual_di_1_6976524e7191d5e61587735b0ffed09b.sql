CREATE TABLE [3e11f521-d002-4710-9f4f-55c488cfd03f].[visual_di_1_6976524e7191d5e61587735b0ffed09b] (
    [id]                                                              BIGINT           IDENTITY (1, 1) NOT NULL,
    [rowId]                                                           NVARCHAR (255)   NOT NULL,
    [colId]                                                           NVARCHAR (255)   NOT NULL,
    [scenarioId]                                                      INT              NULL,
    [filterContextHash]                                               NVARCHAR (255)   NULL,
    [updatedAt]                                                       INT              NOT NULL,
    [updatedBy]                                                       NVARCHAR (128)   NOT NULL,
    [dim_DimProductHProductHierarchyDimProductClassName]              NVARCHAR (255)   NULL,
    [dim_DimProductHProductHierarchyDimProductBrandName]              NVARCHAR (255)   NULL,
    [dim_DimProductHProductHierarchyDimProductProductCategoryName]    NVARCHAR (255)   NULL,
    [dim_DimProductHProductHierarchyDimProductProductSubcategoryName] NVARCHAR (255)   NULL,
    [dim_DimProductHProductHierarchyDimProductProductName]            NVARCHAR (255)   NULL,
    [measure_1]                                                       DECIMAL (30, 10) NULL,
    [measure_2]                                                       DECIMAL (30, 10) NULL,
    [measure_3]                                                       NVARCHAR (MAX)   NULL,
    [measure_1_meta]                                                  NVARCHAR (255)   NULL,
    [measure_2_meta]                                                  NVARCHAR (255)   NULL,
    [measure_3_meta]                                                  NVARCHAR (255)   NULL,
    PRIMARY KEY CLUSTERED ([id] ASC),
    UNIQUE NONCLUSTERED ([rowId] ASC, [colId] ASC, [scenarioId] ASC, [filterContextHash] ASC)
);


GO


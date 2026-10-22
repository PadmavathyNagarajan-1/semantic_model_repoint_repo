CREATE TABLE [8a580838-3856-4c02-8df8-2a3c4403df41].[visual_di_1_6976524e7191d5e61587735b0ffed09b] (
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
    [measure_1_meta]                                                  NVARCHAR (255)   NULL,
    [measure_2_meta]                                                  NVARCHAR (255)   NULL,
    [measure_4]                                                       NVARCHAR (MAX)   NULL,
    [measure_4_meta]                                                  NVARCHAR (255)   NULL,
    [measure_5]                                                       DECIMAL (30, 10) NULL,
    [measure_5_meta]                                                  NVARCHAR (255)   NULL,
    [measure_10]                                                      NVARCHAR (MAX)   NULL,
    [measure_10_meta]                                                 NVARCHAR (255)   NULL,
    PRIMARY KEY CLUSTERED ([id] ASC),
    UNIQUE NONCLUSTERED ([rowId] ASC, [colId] ASC, [scenarioId] ASC, [filterContextHash] ASC)
);


GO


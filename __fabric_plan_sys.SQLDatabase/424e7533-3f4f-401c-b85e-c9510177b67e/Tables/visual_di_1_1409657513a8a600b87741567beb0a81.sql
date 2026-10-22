CREATE TABLE [424e7533-3f4f-401c-b85e-c9510177b67e].[visual_di_1_1409657513a8a600b87741567beb0a81] (
    [id]                                BIGINT           IDENTITY (1, 1) NOT NULL,
    [rowId]                             NVARCHAR (255)   NOT NULL,
    [colId]                             NVARCHAR (255)   NOT NULL,
    [scenarioId]                        INT              NULL,
    [filterContextHash]                 NVARCHAR (255)   NULL,
    [updatedAt]                         INT              NOT NULL,
    [updatedBy]                         NVARCHAR (128)   NOT NULL,
    [dim_Financial_DataCustomerSegment] NVARCHAR (255)   NULL,
    [measure_1]                         DECIMAL (30, 10) NULL,
    [measure_1_meta]                    NVARCHAR (255)   NULL,
    PRIMARY KEY CLUSTERED ([id] ASC),
    UNIQUE NONCLUSTERED ([rowId] ASC, [colId] ASC, [scenarioId] ASC, [filterContextHash] ASC)
);


GO


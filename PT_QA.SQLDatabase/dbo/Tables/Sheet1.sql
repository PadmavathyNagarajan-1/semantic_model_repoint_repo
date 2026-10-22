CREATE TABLE [dbo].[Sheet1] (
    [productId]     INT           NOT NULL,
    [ProductName]   VARCHAR (255) NULL,
    [Category]      VARCHAR (255) NULL,
    [Price]         FLOAT (53)    NULL,
    [StockQuantity] INT           NULL,
    [Manufacturer]  VARCHAR (255) NULL,
    [Supplier]      VARCHAR (255) NULL,
    [Rating]        FLOAT (53)    NULL,
    [Discount]      FLOAT (53)    NULL,
    [ReleaseDate]   DATE          NULL,
    [Color]         VARCHAR (255) NULL,
    [Dimensions]    VARCHAR (255) NULL,
    [Weight]        FLOAT (53)    NULL,
    [IsAvailable]   VARCHAR (255) NULL,
    CONSTRAINT [PK_Sheet1_productId_ebaa6b0391] PRIMARY KEY CLUSTERED ([productId] ASC)
);


GO


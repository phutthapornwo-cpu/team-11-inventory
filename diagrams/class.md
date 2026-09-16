classDiagram
    class TransactionType {
        <<enumeration>>
        RECEIVE
        ISSUE
    }

    class Product {
        +int id
        +str name
        +str category
        +int quantity
        +int threshold
        +Optional~float~ unit_price
        +__post_init__() void
    }

    class StockTransaction {
        +int transaction_id
        +int product_id
        +TransactionType type
        +int quantity
        +int stock_before
        +int stock_after
        +datetime timestamp
    }

    class Notifier {
        <<interface>>
        +send(message: str) void
    }

    class EmailNotifier {
        +send(message: str) void
    }

    class SMSNotifier {
        +send(message: str) void
    }

    class NotifierFactory {
        -Dict~str, Type~Notifier~~ _registry$
        +register_notifier(channel_name: str, notifier_cls: Type~Notifier~) void$
        +create(channel_name: str) Notifier$
    }

    class InventoryService {
        +Dict~int, Product~ products
        +List~StockTransaction~ transactions
        +List~Notifier~ notifiers
        -int _next_tx_id
        +add_product(product: Product) void
        +set_threshold(product_id: int, new_threshold: int) void
        +receive_stock(product_id: int, quantity: int) StockTransaction
        +issue_stock(product_id: int, quantity: int) StockTransaction
        -_notify_low_stock(product: Product) void
    }

    class ReportService {
        +InventoryService inventory_service
        +get_stock_value_report() Dict~str, float~
    }

    %% Realization (Implementation)
    Notifier <|.. EmailNotifier : realization
    Notifier <|.. SMSNotifier : realization

    %% Composition & Aggregation
    StockTransaction *-- TransactionType : composition[cite: 3]
    InventoryService *-- Product : composition
    InventoryService *-- StockTransaction : composition[cite: 3, 5]

    %% Dependency & Association
    InventoryService o-- Notifier : aggregation / dependency
    ReportService --> InventoryService : association / dependency
    NotifierFactory ..> Notifier : creates / dependency
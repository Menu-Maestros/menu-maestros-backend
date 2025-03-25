CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name TEXT,  -- Nullable for guest users
    email TEXT UNIQUE,  -- Nullable for guest users
    password TEXT,  -- Nullable for guest users
    user_type TEXT CHECK (user_type IN ('customer', 'restaurant_worker', 'admin', 'table', 'totem')),

    active BOOLEAN DEFAULT TRUE,

    address TEXT,
    city TEXT,
    state TEXT,
    zip_code TEXT
    
    created_at TIMESTAMP DEFAULT NOW(),
);

CREATE TABLE menu_items (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name TEXT NOT NULL,
    description TEXT,
    price DECIMAL(10,2) NOT NULL,
    image_url TEXT,
    category TEXT NOT NULL CHECK (category IN ('food', 'drink', 'dessert', 'other')),
    available BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE orders (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name TEXT,
    user_id UUID REFERENCES users(id) ON DELETE SET NULL,
    status TEXT CHECK (status IN ('pending', 'preparing', 'ready', 'completed', 'cancelled')) DEFAULT 'pending',
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE order_items (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    order_id UUID REFERENCES orders(id) ON DELETE CASCADE,
    menu_item_id UUID REFERENCES menu_items(id) ON DELETE CASCADE,
    quantity INT CHECK (quantity > 0) NOT NULL,
    price DECIMAL(10,2) NOT NULL,
    created_at TIMESTAMP DEFAULT NOW()
);
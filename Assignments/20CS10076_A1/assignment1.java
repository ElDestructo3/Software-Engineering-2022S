import java.util.*;
                                                                                          // for simplicty, I have assumed that product is an entity
class Entity {                                                                            // defining the class Entity with constructor and functions to obtain class variables
    private int ID;                                                                       
    private String name;

    public Entity(int ID, String name) {
        this.ID = ID;
        this.name = name;
    }

    public int getID() {
        return this.ID;
    }

    public String getName() {
        return this.name;
    }

}

class Manufacturer extends Entity {                                                       // defining manufacturer class to entend entity with an array for storing products sold and the number of unique products
    private Entity ProductsManufactured[];
    private int numProducts;

    public Manufacturer(int ID, String name) {                                            // constructor to initialize the manufacturer class
        super(ID, name);
        this.ProductsManufactured = new Entity[10];
        this.numProducts = 0;                  
    }

    public void addProducts(Entity product) {                                            // adding products, assuming an upper limit of 10 products
        
        if (numProducts < 10) {
            ProductsManufactured[numProducts] = product;
            numProducts++;
        } 
        
        else {
            System.out.println("Manufacturer is full");
        }
    }

    public void printProducts() {                                                        // printing the products manufactured by the manufacturer
        System.out.println("Manufacturer " + this.getName() + " manufactures the following products:");
        for (int i = 0; i < numProducts; i++) {
            System.out.println(ProductsManufactured[i].getName());
        }
    }

    public int getNumProducts() {
        return this.numProducts;
    }

    public void deleteProducts(Entity product) {                                         // deleting a particular product from the array, with checks for presence of product 

        if (this.numProducts == 0) {
            System.out.println("Manufacturer is empty");
        } 
        
        else {
            for (int i = 0; i < this.numProducts; i++) {
                if (ProductsManufactured[i].getName().equals(product.getName())) {
                    for (int j = i; j < this.numProducts - 1; j++) {
                        ProductsManufactured[j] = ProductsManufactured[j + 1];
                    }
                    this.numProducts--;
                    return;
                }
            }
            System.out.println("Product not found");
        }

    }
}

class Customer extends Entity {                                                         // customer class which extends entity class to store zipcode, an array of products bought, and counter for number of products
    private int zipcode; 
    private Entity ProductsBought[];
    private int numProducts;

    public Customer(int ID, String name, int zipcode) {                                // constructor
        super(ID, name);
        this.zipcode = zipcode;
        this.ProductsBought = new Entity[10];
    }
 
    public void addProducts(Entity product) {                                          // add products to inventory checking for upper bound of 10
        if (numProducts < 10) {
            ProductsBought[numProducts] = product;
            numProducts++;
        }
        
        else {
            System.out.println("You have reached the maximum limit for the number of orders.");
        }
    }

    public int getZipcode() {
        return this.zipcode;
    }

    public int getNumProducts() {
        return this.numProducts;
    }

    public void printProducts() {                                                       // similar functions for printing and deleting products, with checks for validity
        System.out.println("Customer " + this.getName() + " bought the following products:");
        for (int i = 0; i < numProducts; i++) {
            System.out.println(ProductsBought[i].getName());
        }
    }

    public void deleteProducts(Entity product) {
        if (this.numProducts == 0) {
            System.out.println("Customer has not bought any products.");
        } 
        
        else {
            for (int i = 0; i < this.numProducts; i++) {
                if (ProductsBought[i].getName().equals(product.getName())) {
                    for (int j = i; j < this.numProducts - 1; j++) {
                        ProductsBought[j] = ProductsBought[j + 1];
                    }
                    this.numProducts--;
                    return;
                }
            }
        }
    }

}

class deliveryAgent extends Entity {                                                         // a class for delivery agent extending entity, storing zipcode and number of products delivered
    private int zipcode;
    private int numberProductsDelivered;

    public deliveryAgent(int ID, String name, int zipcode) {                                // constructor and other utility functions for member variables 
        super(ID, name);
        this.zipcode = zipcode;
        this.numberProductsDelivered = 0;
    }

    public int getZipcode() {
        return this.zipcode;
    }

    public int getNumProductsDelivered() {
        return this.numberProductsDelivered;
    }

    public void addProductsDelivered(Entity product) {                                       // incrmenting counter on being matched for delivery
        this.numberProductsDelivered++;
    }
}

class Pair<String, Integer> {                                                               // defining custom pair class to be used for storing products at a shop or warehouse
    private String key;
    private Integer value;

    public Pair(String key, Integer value) {
        this.key = key;
        this.value = value;
    }

    public String getKey() {
        return this.key;
    }

    public Integer getValue() {
        return this.value;
    }

    public void setKey(String key) {
        this.key = key;
    }

    public void setValue(Integer value) {
        this.value = value;
    }

}



class shopsAndWarehouse extends Entity {                                                       // a class for shops/warehouse extending entity, storing products inventory, number of unique products and zipcode
    private int zipcode;
    private Set<Pair<String, Integer>> ProductsInStock;                                        // using a set to prevent duplicate entries from being added to the inventory
    private int numProducts;

    public shopsAndWarehouse(int ID, String name, int zipcode) {                              // constructor and other utility functions for member variables, printing, adding and deleting products
        super(ID, name);
        this.zipcode = zipcode;
        this.ProductsInStock = new HashSet<>();
        this.numProducts = 0;
    }

    public int getZipcode() {
        return this.zipcode;
    }

    public int getNumProducts() {
        return this.numProducts;
    }
    
    public Set<Pair<String, Integer>> getProductsInStock() {
        return this.ProductsInStock;
    }
    public void addProducts(Entity product, int quantity) {

        int flag = 0;
        for (Pair<String, Integer> p : ProductsInStock) {                                      // adding products to inventory, checking for duplicate entries
            if (p.getKey().equals(product.getName())) {
                p.setValue(p.getValue() + quantity);
                flag = 1;
            }
        }

        if (flag == 0) {
            Pair<String, Integer> p = new Pair<String, Integer>(product.getName(), quantity);
            ProductsInStock.add(p);
            this.numProducts++;
        }

    }
 
    public void updatePurchase(Entity product, int quantity) {                                 // updating the inventory after a purchase
        for (Pair<String, Integer> p : ProductsInStock) { 
            if (p.getKey().equals(product.getName())) {
                p.setValue(p.getValue() - quantity);
                return;
            }
        }
    }

    public void deleteProducts(Entity product) {
        if (this.numProducts == 0) {
            System.out.println("Shop/Warehouse is empty");
        }
        
        else {
            for (Pair<String, Integer> pair : this.ProductsInStock) {
                if (pair.getKey().equals(product.getName())) {
                    this.ProductsInStock.remove(pair);
                    this.numProducts--;
                    return;
                }
            }
            System.out.println("Product not found");
        }
    }

    public void printProducts() {
        System.out.println("Shop/Warehouse " + this.getName() + " has the following products:");
        for (Pair<String, Integer> pair : this.ProductsInStock) {
            System.out.println(pair.getKey() + " : " + pair.getValue());
        }
    }
}

public class assignment0 {
    

    public static void main(String[] args) {

        Set<Manufacturer> Manufacturers = new HashSet<>();                       // creating sets for storing lists of maufacturers, customers, delivery agents and shops/warehouses
        Set<Customer> Customers = new HashSet<>();
        Set<deliveryAgent> deliveryAgents = new HashSet<>();
        Set<shopsAndWarehouse> shopsAndWarehouses = new HashSet<>();

        System.out.println("Welcome to ABC General Store.");                    // creating checks for each type of entity
        System.out.println("If you are a customer, press 1. If you are a manufacturer, press 2. If you are a delivery agent, press 3. If you are a shop/warehouse owner, press 4. If you want to exit, press 5.");
        Scanner sc = new Scanner(System.in);                                    // creating a scanner object
        int entityChoice = sc.nextInt();
        while (entityChoice!=5) {                                               // keep on running until entity exits
            if (entityChoice == 1) {
                System.out.println("Welcome to ABC General Store, dear customer.");
          
                System.out.println("Please enter your name:");                  // accepting details from customer
                String name = sc.next(); 
                System.out.println("Please enter your ID(Create your own ID if you are new to this shop):");
                int ID = sc.nextInt();
                System.out.println("Please enter your zipcode:");
                int zipcode = sc.nextInt();
                Customer customer=null;
                int flag=0;
                for (Customer c : Customers) {                                  // checking the set of customers to identify if the customer is already present
                    if (c.getName().equals(name)&&c.getID()==ID) {
                        customer = c;                                           // capturing details of the customer if present
                        System.out.println("Customer identified successfully.");
                        flag=1;
                        break;
                        
                    }
    
            
                }
                if (flag==0) {
                    customer = new Customer(ID, name, zipcode); 
                    Customers.add(customer);                                   // adding customer to the set
                    System.out.println("Customer added successfully.");
                    
                }
    

                System.out.println("If you want to buy a product, press 1. If you want to see the list of products bought by you before, press 2. If you want to delete your record, press 3.");
                int customerChoice = sc.nextInt(); 
                if (customerChoice== 1) {                                     // processing Order
                    System.out.println("Please enter the name of the product you want to buy:");       // taking details of product to be purchased
                    String ProductName = sc.next();
                    System.out.println("Please enter the ID of the product you want to buy:");
                    int ProductID = sc.nextInt();
                    
                    System.out.println("Please enter the quantity of the product you want to buy:");
                    int quantity = sc.nextInt(); 
                    Entity product = new Entity(ProductID, ProductName);           // creating product object
                    flag=1; 
    
                    for (shopsAndWarehouse s : shopsAndWarehouses) {           // checking if the product is present in the shops/warehouses of the customer's zipcode
                        if (s.getZipcode()!=zipcode) {
                            continue;
                        }
                        for (Pair<String, Integer> p : s.getProductsInStock()) {
                            if (p.getKey().equals(ProductName)) {
                                flag=0;
                                if (p.getValue() >= quantity) {                // checkiing if quantity is sufficient
                                    
                                    
                                    int min=Integer.MAX_VALUE;
                                    
                                    deliveryAgent agent=null;                 // checking if there is a delivery agent in the zipcode, and with minimum orders delivered
                                    for (deliveryAgent d : deliveryAgents) {
                                        if (d.getZipcode()==zipcode) {
                                            
                                            if (d.getNumProductsDelivered()<min) {
                                                min=d.getNumProductsDelivered();
                                                agent=d;
                                                
                                                
                                            }
                                        }
                                    }
                                    if (agent==null) {                         // exiting if no agent found
                                        System.out.println("No delivery agent found in your area. Sorry for the inconvenience.");
                                    }
                                    else {                                     // updating the details of customer, shop/warehouse and agent
                                        customer.addProducts(product);
                                        s.updatePurchase(product, quantity);
                                        agent.addProductsDelivered(product);
                                        System.out.println("You have been matched with the delivery agent "+agent.getName()+". His ID is "+agent.getID()+". Thank you for shopping with us.");
                                    }
                                    
                                }
                                else {                                         // exiting if quantity is not sufficient
                                    System.out.println("Not enough products in stock. Sorry for the inconvenience.");
                                    
                                    break;
                                }
                            }
                        }
                    }
    
                    if (flag==1) {                                             // exiting if product not found
                        System.out.println("This product is not manufactured by any shop of the zipcode provided. Sorry for the inconvenience.");
                    }
                    
                    
                }
    
                else if (customerChoice == 2) {
                    customer.printProducts();                                                       // showing products bought
                    System.out.println("Products list printed. Thank you for using this platform.");
                }
    
                else if (customerChoice == 3) {
                    customer.printProducts();
                    System.out.println("Choose the product you want to delete. Enter name:");       // Deleting a product after showing list
                    String ProductName = sc.next();
                    System.out.println(" Enter ID:");
                    int ProductID = sc.nextInt();
                    Entity product = new Entity(ProductID, ProductName);
                    customer.deleteProducts(product);
                    System.out.println("Product deleted. Thank you for using this platform.");
                }
    
                else {
                    System.out.println("Invalid input.");
                }
    
            }
    
            else if (entityChoice == 2) {
                System.out.println("Enter password:");
                String password = sc.next();
                if (password.equals("abc")) {                                                       // providing security check for manufacturer
                    System.out.println("Welcome to ABC General Store, dear manufacturer.");
     
                    System.out.println("Please enter your name:");                                  // following similar process for adding to existing set
                    String name = sc.next();
                    System.out.println("Please enter your ID(Create your own ID if you are new to this shop):");
                    int ID = sc.nextInt();
                    Manufacturer manufacturer=null;
                    int flag=0;
                    
                    for (Manufacturer m : Manufacturers) {
                        if (m.getName().equals(name)&&m.getID()==ID) {
                            manufacturer=m;
                            System.out.println("Manufacturer identified successfully.");
                            flag=1;
                            break;
                        }
    
                       
                    }
    
                    if (flag==0) {
                        manufacturer = new Manufacturer(ID, name);
                        System.out.println("Manufacturer added successfully.");
                        Manufacturers.add(manufacturer);
                        
                    }
    
                    
                    
                    
    
                    System.out.println("If you want to add a product, press 1. If you want to see the list of products you have, press 2. If you want to delete your record, press 3.");
                    int manufacturerChoice = sc.nextInt();                                             // adding, printing and deleting products from manufacturer
                    if (manufacturerChoice == 1) {
                        System.out.println("Please enter the name of the product you want to add:");
                        String ProductName = sc.next();
                        System.out.println("Please enter the ID of the product you want to add:");
                        int ProductID = sc.nextInt();
                        Entity product = new Entity(ProductID, ProductName);
                        manufacturer.addProducts(product);
                        System.out.println("Product added. Thank you for using this platform.");
                        manufacturer.printProducts();
                        
                    }
    
                    else if (manufacturerChoice == 2) {
                        
                        manufacturer.printProducts();
                        System.out.println("Thank you for using this platform.");
                    }
    
                    else if (manufacturerChoice == 3) {
                        
                        manufacturer.printProducts();
                        System.out.println("Choose the product you want to delete. Enter name:");
                        String ProductName = sc.next();
                        System.out.println(" Enter ID:");
                        int ProductID = sc.nextInt();
                        Entity product = new Entity(ProductID, ProductName);
                        manufacturer.deleteProducts(product);
                        System.out.println("Product deleted. Thank you for using this platform.");
                    }
    
                    else {
                        System.out.println("Invalid input.");
                    }
                }
    
                else {
                    System.out.println("Wrong password.");
                    
                }
            }
    
            else if (entityChoice == 3) {
                System.out.println("Enter password:");
                String password = sc.next();
                if (password.equals("def")) {                                              // security check for delivery agent
                    System.out.println("Welcome to ABC General Store, dear agent.");
                    
                    
                    System.out.println("Please enter your name:");                    // following similar process for adding to existing set
                    String name = sc.next();
                    System.out.println("Please enter your zipcode:");
                    int zipcode = sc.nextInt();
                    System.out.println("Please enter your ID:");
                    int ID = sc.nextInt();
                    deliveryAgent deliveryAgent=null;
                    int flag=0;
                    for (deliveryAgent d : deliveryAgents) {
                    if (d.getName().equals(name)&&d.getZipcode()==zipcode&&d.getID()==ID) {
                            deliveryAgent=d;
                            System.out.println("Delivery agent idenitfied successfully.");
                            flag=1;
                            break;
                                
                            }
                            
                    }
    
                    if (flag==0) {
                        deliveryAgent = new deliveryAgent(ID, name, zipcode);
                        System.out.println("Delivery agent added successfully.");
                        deliveryAgents.add(deliveryAgent);
                            
                    }
    
                    System.out.println("Thank you for using this platform.");
 
                }
    
                else {
                    System.out.println("Wrong password.");
                    
                }
            }
    
            else if (entityChoice== 4) {
                System.out.println("Enter password:");
                String password = sc.next();
                if (password.equals("ghi")) {                                               // security check for shop/warehouse owner
                    System.out.println("Welcome to ABC General Store, dear owner.");        // following similar process for adding to existing set
                    System.out.println("Please enter your name:"); 
                    String name = sc.next();
                    System.out.println("Please enter your ID:");
                    int ID = sc.nextInt();
                    System.out.println("Please enter your zipcode:");
                    int zipcode = sc.nextInt();
                    shopsAndWarehouse ShopAndWarehouse=null;
                    int flag=1;
                    for (shopsAndWarehouse s : shopsAndWarehouses) {
                        if (s.getName().equals(name)&&s.getID()==ID) {
                            ShopAndWarehouse=s;
                            flag=0;
                            break;
                        }
    
                    }

                    if (flag==0) {
                        System.out.println("Shop/Warehouse identified successfully.");
                    }
                    else {
                        ShopAndWarehouse = new shopsAndWarehouse(ID, name, zipcode);
                        shopsAndWarehouses.add(ShopAndWarehouse);
                        System.out.println("Shop/Warehouse added successfully.");
                    }
                    
                    
                    System.out.println("If you want to add a product, press 1. If you want to see the list of products you have, press 2. If you want to delete a record, press 3.");
                    int shopAndWareHouseChoice = sc.nextInt();
                    if (shopAndWareHouseChoice == 1) {
                        System.out.println("Please enter the name of the product you want to add:");
                        String ProductName = sc.next();
                        System.out.println("Please enter the ID of the product you want to add:");
                        int ProductID = sc.nextInt();
                        System.out.println("Please enter the quantity of the product you want to add:");
                        int quantity = sc.nextInt();
                        Entity product = new Entity(ProductID, ProductName);
                        ShopAndWarehouse.addProducts(product, quantity);
                        System.out.println("Product added. Thank you for using this platform.");
                        
                    }
    
                    else if (shopAndWareHouseChoice == 2) {
                        
                        ShopAndWarehouse.printProducts();
                        System.out.println("Products list printed. Thank you for using this platform.");
                    }
    
                    else if (shopAndWareHouseChoice == 3) {
                        
                        ShopAndWarehouse.printProducts();
                        System.out.println("Choose the product you want to delete. Enter name:");
                        String ProductName = sc.next();
                        System.out.println(" Enter ID:");
                        int ProductID = sc.nextInt();
                        Entity product = new Entity(ProductID, ProductName);
                        ShopAndWarehouse.deleteProducts(product);
                        System.out.println("Product deleted. Thank you for using this platform.");
                    }
    
                    else {
                        System.out.println("Invalid input.");
                    }
                    
                    
    
                    
                }
            }
            System.out.println("If you are a customer, press 1. If you are a manufacturer, press 2. If you are a delivery agent, press 3. If you are a shop/warehouse owner, press 4. If you want to exit, press 5.");
            entityChoice = sc.nextInt();
        }
        System.out.println("Thank you for using ABC General Store. Have a nice day!");
        sc.close();
    }
}

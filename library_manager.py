# JSON ek format hai jisse hum Python objects (jaise lists, dictionaries) ko files mein save kar sakte
# pyhton main built-in module hai json issay hum file main data save krtay hai or file say data load krtay.
import json


class BookCollection:

    """A class too manage a collection of books, allowing users to store and organize their reading materials."""

    # object ko initialize krdiya.
    def __init__(self):
        """Initialize a new book collection with an empty list and set up file storage."""
        # har naye object ke liye ek khaali list banai gayi hai jismein future mein boos kke records (jaise dictionaries) store honge abhi empty hai.
        self.book_list = [] # empty list.
        # self.storage_file: Ye woh file ka naam hai jahan data save hoga (books_data.json). Data ko save rakhna taa ke program band hone ke baad bhi aapki library rahe.
        self.storage_file = 'books_data.json' 
        self.read_from_file() # Yeh function call karta hai jo file se pehle se stored books ko read karta hai.
    
    # yeh method books_data.json file main agar data hai tw jb hum first time run krein gay object banainge tw humein stored data agr waki hai
    # tw humein load krkay deday ga werna empty list hee initialize hogi phir hum khud books ka data store krdein gay.
    def read_from_file(self):
        '''Load saved books from a JSON file into memory. if file does'nt exist or is corrupted, start with an empty collection'''
        #try: file ko open krkay usmain say data load kro json.load(file).
        try:
            # Opening the File in read Mode
            with open(self.storage_file, 'r') as file: 
                self.book_list = json.load(file)
        #except: Agar file nahi mili (FileNotFoundError) ya data kharab hai (JSONDecodeError), toh khali list banao.
        except(FileNotFoundError, json.JSONDecodeError):
            self.book_list = []

    # Data Ko File Mein Save Karna.
    def save_to_file(self):
        '''store the current book collection to a json file for permanent storage'''
        # Opening the File in Write Mode
        with open(self.storage_file, 'w') as file:
            # json.dump() function use hota hai data ko JSON format mein convert karke file mein likhne ke liye.
            #Yeh optional parameter hai jo JSON data ko "pretty-print" karta hai. Matlab, har nested level ke baad 4 spaces insert karta hai, jisse file ka format clean aur readable ho jata hai.
            json.dump(self.book_list, file, indent=4)
    
    # Nayi Kitab Add Karna
    def create_new_book(self):
        '''Add a new book to the collection by gathering information from the user.'''

        # User se inputs lerahay
        book_title = input('Enter book title: ')
        book_author = input('Enter book author: ')
        publication_year = input('Enter book year: ')
        book_gener = input('Enter gener: ')
        # isbookread main true ya false milayga.
        # Yeh function input ke shuru aur akhir se extra spaces hata deta hai. Misal: Agar user " yes " likhe, to strip karne ke baad "yes" ho jayega.
        isbook_read =(
            input('Have u read this book? (yes/no): ').strip().lower() == 'yes'
        ) 

        # Ek dictionary (new_book) banakar upper user kee dui hui detail store krdein.
        new_book: dict = { 
            'title' : book_title,
            'author' : book_author,
            'year' : publication_year,
            'gener' : book_gener,
            'read' : isbook_read
        }
        
        # dictionary ko list main add/store krrahay append method say jo list kay sath use hota hai.
        self.book_list.append(new_book)
        self.save_to_file() # update ko file main save krdiya.
        print('Book added successfully!\n') # success msg dikhana.

    def delete_book(self):
        '''Remove a book from the collection using its title.'''

        # User se book ka title input liya jo book woo delete krna chahta hai.
        book_title = input('Enter title of book you want to remove: ') 
        
        # booklist main moojood sb books pay loop chalaya takay 1 by 1 user kay title say sb books ka title match krskein
        # hum har kitab ka title compare kar saken jo user ne diya hai ussay.
        for book in self.book_list:
            # Jab hm ek book ko represent karne ke liye dict use karte hain, to us dict ke andar keys hoti hain, jaise "title", "author", etc.
            # book['title'] Yeh dictionary se title value access karne ka tarika hai. Yeh use hota hai jab aapko har book ke title ko check ya modify karna ho.
            if book['title'].lower() == book_title.lower():
                self.book_list.remove(book) # Agar condition true ho jati hai, to current kitab (book) ko list se remove krdo
                self.save_to_file() # Is ke baad updated list ko file mein save kar diya jata hai, taa ke permanent storage update ho jaye.
                print("Book removed successfully!\n")
                return # Yeh line method ko turant exit kar deti hai. Jab matching kitab mil jati hai aur remove ho jati hai, 
                       # to further iterations ya niche ka code (jo "Book not found!" print karta hai) run nahi hota.
        print("Book not found!\n") # yeh line loop say bahr hai jb loop poora chalay or koi book na remove hoo tb yeh chalay ga.

    # books ko list main find krna jo books user find krna chahta.
    def find_books(self):
        '''Search for books in collection by title and author'''

        search_type = input('Search by:\n1. title\n2. author\n Enter your choice: ') # 2 options dikhana
        search_text = input('Enter search term: ').lower() # Yeh line user se "search term" (jaise koi kitab ka naam ya author) puchti hai.

        # List comprehension ek concise (chhota aur seedha) syntax hai Python mein jo aapko ek nayi list banane ka tareeqa deta hai.
        # Iska matlab yeh hai ke aap ek hi line mein loop, condition aur transformation use karke list create kar sakte hain 
        found_books = [
            book
            for book in self.book_list
            if search_text in book['title'].lower()
            or search_text in book['author'].lower()
        ]
        
        # agar yeh true hai mtlb foundbooks main books hain tw yeh true hoga.
        if found_books:
            print('Matching Books: ')
            
            # book main eik eik krkay item ainge or index main position items kee or position start 1 say hogi qynke enumerate main humnay
            # 1 dedi hai enumerate(found_books, 1) enumerate main foundbooks say 1 1 krkay book main item jainge.
            for index, book in enumerate(found_books, 1):

                reading_status = 'Read' if book['read'] else 'Unread' # read kee hay ya nhi woo store krrahay or print main dikharahay.
                print(
                    f"{index}. {book['title']} by {book['author']} ({book['year']}) - {book['gener']} - {reading_status}\n"
                )
        else:
            print("No matching books found.\n")

    # existing bool ko update modify krnay kayliye.
    def update_book(self):
        '''Modify the details of the existing book in collection'''

        book_title = input('Enter the title of the book u want to edit: ') # user say title input liya book ka title.
        # for loop
        for book in self.book_list:
            # if condition
            if book['title'].lower() == book_title.lower():
                # user input dega tw woo store hojaiga mtlb new title agar empty chorega tw (or) operator kay baad default 
                # mtlb (or book['title']) jo already title hai wohi rahay ga issi strhan year, gener baki sbb isay Optional Input with Or kehtay.
                # python main ya tw truthy hota ya falsy agar user empty chorta tw falsy hoga or (or operator) agli default wali store krayga
                book['title'] = input(f"New title ({book['title']}): ") or book['title']
                book['author'] = input(f"New author ({book['author']}): ") or book['author']
                book['year'] = input(f"New year ({book['year']}): ") or book['year']
                book['gener'] = input(f"New gener ({book['gener']}): ") or book['gener']
                book['read'] = input('Have you read this book? (yes/no)').strip().lower() == 'yes'

                self.save_to_file()
                print('Book updated successfully!\n')
                return # sb modiy honay baad end hojaiga yahan agay nhi jaiga
        print('Book not found\n') # agar book nhi milti tw yeh print.

    def show_all_books(self):
        '''Display all books in the collection with their details'''
        
        # agar book_list khali hai tw enpty show hoga or agay code nhi execute hoga.
        if not self.book_list:
            print('Your collection is empty.\n')
            return
        
        print("Your Book Collection:")

        for index, book in enumerate(self.book_list, 1):
            # har ek book ke liye uski "read" status ko check karti hai. Agar book["read"] True hai, to reading_status ko "Read" set kar
            # diya jata hai; agar False hai, to "Unread" set ho jata hai. Matlab, har iteration mein aapko us specific book ka reading status
            # milta hai, aur phir use print statement ke zariye display kar diya jata hai.
            reading_status = 'Read' if book['read'] else 'Unread'
            print(
                f"{book['title']} by {book['author']} ({book['year']}) - {book['gener']} - {reading_status}"
                )

        print()
    
    # yeh function library mein kitni kitabain hain aur unmein se kitni padh li gayi hain, iska hisaab rakhta hai
    def show_reading_progress(self):
        '''Calculate and display statistics about your reading progress'''

        total_books = len(self.book_list) # total books kitni hain book_list main uski length store krrahay.
        # Har kitaab ke liye jo parhi gayi hai, 1 lo aur un sab ko jama kar do. Aakhri hisaab 'completed_books' mein save ho jae ga.
        # mtlb agar book read hui way hai tw 1 generate krdo issi trhan 3 books tw 3 ones generate or phir sum hoga 3 or 3 store hoga.
        # Python mein sum() ek built-in function hai jo numbers ki kisi bhi sequence (jaise list, tuple, generator) ko jama 
        # (add) kar ke total value return karta hai.
        completed_books = sum(1 for book in self.book_list if book['read'])

        # Is inline if-else expression mein sabse pehle condition check hoti hai. Matlab, Python pehle evaluate karega ke total_books > 0
        # hai ya nahi. Agar ye condition True hai, to expression (completed_books / total_books * 100) calculate hoga, warna 0 return ho jayega.
        completion_rate = (
            (completed_books / total_books * 100) if total_books > 0 else 0
        )

        print(f'Total books in collection: {total_books}')
        print(f'Reading progess: {completion_rate:.2f}%\n')


    # main method jo user ko friendly interface dikhaiga.
    def start_application(self):
        '''Run the main application loop with a user-friendly menu interface'''

        # while True: Infinite Loop banata hai, jisse program tab tak chalta rahega jab tak user Exit na choose kare.
        # Har Method Ke Baad Control Wapis Loop Ke Start Mein Jata Hai: Matlab, method complete hone ke baad, code while True: line
        # par wapis chala jata hai, aur menu dobara print hota hai.
        while True:
            print('📕 Welcome To Your Book Collection Manager!')
            print('1. Add a book')
            print('2. Remove a book')
            print('3. Search for books')
            print('4. Update book details')
            print('5. View all books')
            print('6. View reading progress')
            print('7. Exit')

            user_choice = input('Please choose an option (1 - 7): ')

            if user_choice == '1':
                self.create_new_book()
            elif user_choice == '2':
                self.delete_book()
            elif user_choice == '3':
                self.find_books()
            elif user_choice == '4':
                self.update_book()
            elif user_choice == '5':
                self.show_all_books()
            elif user_choice == '6':
                self.show_reading_progress()
            elif user_choice == '7':
                self.save_to_file()
                print('Thank you for using book collection manager. Goodbye!')
                break # break statement (option 7 mein) loop ko terminate karti ha break statement loop se bahar nikalne ke liye use hoti hai.
            else:
                print('Invalid choice. please try again.\n')

# if __name__ == "__main__": ka matlab hai: "Agar ye file directly run ki gayi hai (python library_manager.py) toh ye code chalao."
# Example: Jaise aap python library_manager.py run karen, toh app start hogi. Agar kisi aur file ne isko import kiya, 
# toh app automatic nahi chalegi.
if __name__ == "__main__":
     book_manager = BookCollection()
     book_manager.start_application()
   
 
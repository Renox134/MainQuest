from journal import Journal
from ui.app import MainQuestApp

if __name__ == "__main__":
    journal: Journal = Journal()
    main_app = MainQuestApp(journal)
    main_app.run()

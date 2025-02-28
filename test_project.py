import pytest
from tkinter import Tk
from project import College_Grade_Management, Login_Grade_Management

@pytest.fixture
def project():
    root = Tk()
    project = College_Grade_Management(root)
    yield project
    root.destroy()

def test_generate_heading(project):
    heading = project.generate_heading(project.root, "Test Heading", ("Arial", 25))
    assert heading.winfo_children()[0].cget("text") == " Test Heading "

def test_status_update(project):
    project.status_update("Test Status", "green")
    assert project.status_text.cget("text") == "Test Status"
    assert project.status_frame.cget("bg") == "green"

def test_clear_status_frame(project):
    project.status_update("Test Status", "green")
    project.clear_status_frame()
    assert len(project.status_frame.winfo_children()) != 0

def test_clear_entry_frame(project):
    project.entry_frame_parent.pack_forget()
    project.clear_entry_frame()
    assert len(project.entry_frame_parent.winfo_children()) == 0

def test_set_up_entry_window(project):
    project.set_up_entry_window("Test Function", ["Field1", "Field2"])
    assert len(project.entry_frame.winfo_children()) == 5  # 2 labels + 2 entries

def test_exit_fullscreen(project):
    project.exit_fullscreen()
    assert not project.fullscreen

if __name__ == "__main__":
    pytest.main()
import time

from selenium import webdriver
import pytest
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.keys import Keys
import re

MAX_TIME = 5


class pytest_regex:
    """Assert that a given string meets some expectations."""

    def __init__(self, pattern, flags=0):
        self._regex = re.compile(pattern, flags)

    def __eq__(self, actual):
        return bool(self._regex.match(actual))

    def __repr__(self):
        return self._regex.pattern


@pytest.fixture
def browser():
    browser = webdriver.Firefox()
    yield browser
    browser.quit()


@pytest.mark.django_db
def test_app_title_is_shown(browser, live_server):
    # Edith has heard about a cool new online to-do app. She goes
    # to check out its homepage
    browser.get(live_server.url)
    # She notices the page title and header mention to-do lists
    assert "To-Do" in browser.title


def wait_for_row_in_list_table(browser, row_text):
    start_time = time.time()
    while True:
        try:
            table = browser.find_element_by_id('id_list_table')
            rows = table.find_elements_by_tag_name('tr')
            assert row_text in [row.text for row in rows]
            return
        except (AssertionError, WebDriverException) as e:
            if time.time() - start_time > MAX_TIME:
                raise e
            time.sleep(0.2)


@pytest.mark.django_db
def test_can_start_a_list_for_one_user(browser, live_server):
    # Edith has heard about a cool new online to-do app. She goes
    # to check out its homepage
    browser.get(live_server.url)
    # She notices the page title and header mention to-do lists
    assert "To-Do" in browser.title
    header_text = browser.find_element_by_tag_name('h1').text
    assert "To-Do" in header_text

    # She is invited to enter a to-do item straight away
    inputbox = browser.find_element_by_id('id_new_item')
    assert inputbox.get_attribute('placeholder') == 'Enter a to-do item'

    # She types "Buy peacock feathers" into a text box (Edith's hobby
    # is tying fly-fishing lures)
    inputbox.send_keys('Buy peacock feathers')

    # When she hits enter, the page updates, and now the page lists
    # "1: Buy peacock feathers" as an item in a to-do list
    inputbox.send_keys(Keys.ENTER)
    # time.sleep(1)

    wait_for_row_in_list_table(browser, "1: Buy peacock feathers")

    # There is still a text box inviting her to add another item. She
    # enters "Use peacock feathers to make a fly" (Edith is very methodical)
    inputbox = browser.find_element_by_id('id_new_item')
    inputbox.send_keys('Use peacock feathers to make a fly')
    inputbox.send_keys(Keys.ENTER)
    # time.sleep(1)

    # The page updates again, and now shows both items on her list
    wait_for_row_in_list_table(browser, "1: Buy peacock feathers")
    wait_for_row_in_list_table(browser, "2: Use peacock feathers to make a fly")

    # Edith wonders whether the site will remember her list. Then she sees
    # that the site has generated a unique URL for her -- there is some
    # explanatory text to that effect.

    # She visits that URL - her to-do list is still there.

    # Satisfied, she goes back to sleep


def test_multiple_users_can_start_lists_at_different_urls(browser, live_server):
    # Edith has heard about a cool new online to-do app. She goes
    # to check out its homepage
    browser.get(live_server.url)
    # She is invited to enter a to-do item straight away
    inputbox = browser.find_element_by_id('id_new_item')
    # She types "Buy peacock feathers" into a text box (Edith's hobby
    # is tying fly-fishing lures)
    inputbox.send_keys('Buy peacock feathers')
    inputbox.send_keys(Keys.ENTER)
    wait_for_row_in_list_table(browser, "1: Buy peacock feathers")

    # She notices that her list has a unique URL
    edith_list_url = browser.current_url
    assert edith_list_url == pytest_regex("^.*/lists/.+")

    # Now a next user francis comes along on the site

    # We use a new browser session to make sure that no information
    # of Edith's is coming from browser cookies
    browser.quit()
    new_browser = webdriver.Firefox()

    # Francis visits home page and there is no sign of Edith's data
    new_browser.get(live_server.url)
    page_text = new_browser.find_element_by_tag_name('body').text

    assert "Buy peacock feathers" not in page_text

    # Francis starts a new list by entering a new item
    inputbox = new_browser.find_element_by_id('id_new_item')
    inputbox.send_keys('Buy milk')
    inputbox.send_keys(Keys.ENTER)
    wait_for_row_in_list_table(new_browser, '1: Buy milk')

    # Francis gets his own unique URL
    francis_list_url = new_browser.current_url
    assert francis_list_url == pytest_regex("^.*/lists/.+")
    assert francis_list_url != edith_list_url

    # Again there is no trace of Edith's list
    page_text = new_browser.find_element_by_tag_name('body').text
    assert 'Buy peacock feathers' not in page_text
    assert 'Buy milk' in page_text

    # satisfied they both goback to sleep


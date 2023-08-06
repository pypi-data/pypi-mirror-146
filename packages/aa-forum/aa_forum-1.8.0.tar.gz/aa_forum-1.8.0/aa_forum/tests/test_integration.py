# Standard Library
import json
from unittest.mock import patch

# Third Party
import requests
from django_webtest import WebTest

# Django
from django.urls import reverse

# AA Forum
from aa_forum.models import Board, Category, Message, Topic
from aa_forum.tests.utils import (
    create_fake_message,
    create_fake_messages,
    create_fake_user,
)


class TestForumUI(WebTest):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user_1001 = create_fake_user(
            1001, "Bruce Wayne", permissions=["aa_forum.basic_access"]
        )
        cls.user_1002 = create_fake_user(
            1002, "Peter Parker", permissions=["aa_forum.basic_access"]
        )
        cls.user_1003 = create_fake_user(1003, "Lex Luthor", permissions=[])
        cls.category = Category.objects.create(name="Science")
        cls.board = Board.objects.create(name="Physics", category=cls.category)
        cls.board_with_webhook = Board.objects.create(
            name="Chemistry",
            category=cls.category,
            discord_webhook="https://discord.com/webhook/",
        )
        cls.board_with_webhook_for_replies = Board.objects.create(
            name="Biology",
            category=cls.category,
            discord_webhook="https://discord.com/webhook/",
            use_webhook_for_replies=True,
        )

    def test_should_show_forum_index(self):
        # given
        self.app.set_user(self.user_1001)
        # when
        page = self.app.get(reverse("aa_forum:forum_index"))
        # then
        self.assertTemplateUsed(page, "aa_forum/view/forum/index.html")

    def test_should_not_show_forum_index(self):
        # given
        self.app.set_user(self.user_1003)
        # when
        page = self.app.get(reverse("aa_forum:forum_index"))
        # then
        self.assertRedirects(page, "/account/login/?next=/forum/")

    def test_should_create_new_topic(self):
        # given
        self.app.set_user(self.user_1001)
        page = self.app.get(self.board.get_absolute_url())
        # when
        page = page.click(linkid="aa-forum-btn-new-topic-above-list")

        form = page.forms["aa-forum-form-new-topic"]
        form["subject"] = "Recent Discoveries"
        form["message"] = "Energy of the Higgs boson"
        page = form.submit().follow()

        # then
        self.assertEqual(self.board.topics.count(), 1)
        self.assertTemplateUsed(page, "aa_forum/view/forum/topic.html")
        new_topic = Topic.objects.last()
        self.assertEqual(new_topic.subject, "Recent Discoveries")
        new_message = Message.objects.last()
        self.assertEqual(new_message.message, "Energy of the Higgs boson")

    @patch("requests.post")
    def test_should_post_to_discord_webhook_on_create_new_topic(self, mock_post):
        # given
        self.app.set_user(self.user_1001)
        page = self.app.get(self.board_with_webhook.get_absolute_url())

        # when
        page = page.click(linkid="aa-forum-btn-new-topic-above-list")

        form = page.forms["aa-forum-form-new-topic"]
        form["subject"] = "Recent Discoveries"
        form["message"] = "Energy of the Higgs boson"
        page = form.submit().follow()

        # then
        self.assertEqual(self.board_with_webhook.topics.count(), 1)
        self.assertTemplateUsed(page, "aa_forum/view/forum/topic.html")
        new_topic = Topic.objects.last()
        self.assertEqual(new_topic.subject, "Recent Discoveries")
        new_message = Message.objects.last()
        self.assertEqual(new_message.message, "Energy of the Higgs boson")

        info = {"test1": "value1", "test2": "value2"}
        requests.post(self.board_with_webhook.discord_webhook, data=json.dumps(info))
        mock_post.assert_called_with(
            self.board_with_webhook.discord_webhook, data=json.dumps(info)
        )

    @patch("requests.post")
    def test_should_post_to_discord_webhook_with_image_on_create_new_topic(
        self, mock_post
    ):
        # given
        self.app.set_user(self.user_1001)
        page = self.app.get(self.board_with_webhook.get_absolute_url())

        # when
        page = page.click(linkid="aa-forum-btn-new-topic-above-list")

        form = page.forms["aa-forum-form-new-topic"]
        form["subject"] = "Recent Discoveries"
        form[
            "message"
        ] = "Energy of the Higgs boson <img src='/images/images/038/929/227/large/marc-bell-2a.jpg'>"
        page = form.submit().follow()

        # then
        self.assertEqual(self.board_with_webhook.topics.count(), 1)
        self.assertTemplateUsed(page, "aa_forum/view/forum/topic.html")
        new_topic = Topic.objects.last()
        self.assertEqual(new_topic.subject, "Recent Discoveries")
        new_message = Message.objects.last()
        self.assertEqual(
            new_message.message,
            "Energy of the Higgs boson <img src='/images/images/038/929/227/large/marc-bell-2a.jpg'>",
        )

        info = {"test1": "value1", "test2": "value2"}
        requests.post(self.board_with_webhook.discord_webhook, data=json.dumps(info))
        mock_post.assert_called_with(
            self.board_with_webhook.discord_webhook, data=json.dumps(info)
        )

    @patch("requests.post")
    def test_should_post_to_discord_webhook_with_image_with_full_url_on_create_new_topic(
        self, mock_post
    ):
        # given
        self.app.set_user(self.user_1001)
        page = self.app.get(self.board_with_webhook.get_absolute_url())

        # when
        page = page.click(linkid="aa-forum-btn-new-topic-above-list")

        form = page.forms["aa-forum-form-new-topic"]
        form["subject"] = "Recent Discoveries"
        form[
            "message"
        ] = "Energy of the Higgs boson <img src='https://cdnb.artstation.com/p/assets/images/images/038/929/227/large/marc-bell-2a.jpg'>"
        page = form.submit().follow()

        # then
        self.assertEqual(self.board_with_webhook.topics.count(), 1)
        self.assertTemplateUsed(page, "aa_forum/view/forum/topic.html")
        new_topic = Topic.objects.last()
        self.assertEqual(new_topic.subject, "Recent Discoveries")
        new_message = Message.objects.last()
        self.assertEqual(
            new_message.message,
            "Energy of the Higgs boson <img src='https://cdnb.artstation.com/p/assets/images/images/038/929/227/large/marc-bell-2a.jpg'>",
        )

        info = {"test1": "value1", "test2": "value2"}
        requests.post(self.board_with_webhook.discord_webhook, data=json.dumps(info))
        mock_post.assert_called_with(
            self.board_with_webhook.discord_webhook, data=json.dumps(info)
        )

    def test_should_cancel_new_topic(self):
        # given
        self.app.set_user(self.user_1001)
        page = self.app.get(self.board.get_absolute_url())
        # when
        page = page.click(linkid="aa-forum-btn-new-topic-above-list")
        # then
        page = page.click(linkid="aa-forum-btn-cancel")
        # then
        self.assertEqual(self.board.topics.count(), 0)
        self.assertTemplateUsed(page, "aa_forum/view/forum/board.html")

    def test_should_create_reply_in_topic(self):
        # given
        topic = Topic.objects.create(
            subject="Mysteries", board=self.board_with_webhook_for_replies
        )
        create_fake_messages(topic=topic, amount=5)
        self.app.set_user(self.user_1001)
        page = self.app.get(topic.get_absolute_url())

        # when
        form = page.forms["aa-forum-form-message-reply"]
        form["message"] = "What is dark matter?"
        page = form.submit().follow().follow()

        # then
        self.assertEqual(topic.messages.count(), 6)
        self.assertTemplateUsed(page, "aa_forum/view/forum/topic.html")
        new_message = Message.objects.last()
        self.assertEqual(new_message.message, "What is dark matter?")

    def test_should_post_to_webhook_on_create_reply_in_topic(self):
        # given
        topic = Topic.objects.create(subject="Mysteries", board=self.board)
        create_fake_messages(topic=topic, amount=5)
        self.app.set_user(self.user_1001)
        page = self.app.get(topic.get_absolute_url())
        # when
        form = page.forms["aa-forum-form-message-reply"]
        form["message"] = "What is dark matter?"
        page = form.submit().follow().follow()
        # then
        self.assertEqual(topic.messages.count(), 6)
        self.assertTemplateUsed(page, "aa_forum/view/forum/topic.html")
        new_message = Message.objects.last()
        self.assertEqual(new_message.message, "What is dark matter?")

    def test_should_update_own_message(self):
        # given
        topic = Topic.objects.create(subject="Mysteries", board=self.board)
        own_message = create_fake_message(topic=topic, user=self.user_1001)
        self.app.set_user(self.user_1001)
        page = self.app.get(topic.get_absolute_url())
        # when
        page = page.click(linkid=f"aa-forum-btn-modify-message-{own_message.pk}")
        form = page.forms["aa-forum-form-message-modify"]
        form["message"] = "What is dark matter?"
        page = form.submit().follow().follow()
        # then
        self.assertEqual(topic.messages.count(), 1)
        self.assertTemplateUsed(page, "aa_forum/view/forum/topic.html")
        own_message.refresh_from_db()
        self.assertEqual(own_message.message, "What is dark matter?")

    def test_should_not_be_able_to_edit_messages_from_others(self):
        # given
        topic = Topic.objects.create(subject="Mysteries", board=self.board)
        alien_message = create_fake_message(topic=topic, user=self.user_1002)
        self.app.set_user(self.user_1001)
        # when
        page = self.app.get(topic.get_absolute_url())
        # then
        self.assertTemplateUsed(page, "aa_forum/view/forum/topic.html")
        self.assertNotContains(page, f"aa-forum-btn-modify-message-{alien_message.pk}")

    def test_should_find_message_by_key_word(self):
        # given
        topic_1 = Topic.objects.create(subject="Topic 1", board=self.board)
        create_fake_messages(topic=topic_1, amount=5)
        topic_2 = Topic.objects.create(subject="Topic 2", board=self.board)
        create_fake_messages(topic=topic_2, amount=5)
        message = Message.objects.create(
            topic=topic_1, user_created=self.user_1001, message="xyz dummy123 abc"
        )
        self.app.set_user(self.user_1001)
        page = self.app.get(reverse("aa_forum:forum_index"))
        # when
        form = page.forms["aa-forum-form-search-menu"]
        form["q"] = "dummy123"
        res = form.submit()
        # then
        self.assertTemplateUsed(res, "aa_forum/view/search/results.html")
        self.assertContains(
            res,
            reverse(
                "aa_forum:forum_message",
                args=[
                    message.topic.board.category.slug,
                    message.topic.board.slug,
                    message.topic.slug,
                    message.pk,
                ],
            ),
        )


class TestAdminUI(WebTest):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = create_fake_user(
            1001,
            "Bruce Wayne",
            permissions=["aa_forum.basic_access", "aa_forum.manage_forum"],
        )

    def test_should_create_category(self):
        # given
        self.app.set_user(self.user)
        page = self.app.get(reverse("aa_forum:admin_index"))
        # when
        form = page.forms["aa-forum-form-admin-new-category"]
        form["new-category-name"] = "Category"
        page = form.submit().follow()
        # then
        self.assertTemplateUsed(page, "aa_forum/view/administration/index.html")
        new_category = Category.objects.last()
        self.assertEqual(new_category.name, "Category")

    def test_should_edit_category(self):
        # given
        category = Category.objects.create(name="Category")
        self.app.set_user(self.user)
        page = self.app.get(reverse("aa_forum:admin_index"))
        # when
        form = page.forms[f"aa-forum-form-admin-edit-category-{category.pk}"]
        form[f"edit-category-{category.pk}-name"] = "Dummy"
        page = form.submit().follow()
        # then
        self.assertTemplateUsed(page, "aa_forum/view/administration/index.html")
        category.refresh_from_db()
        self.assertEqual(category.name, "Dummy")

    def test_should_add_board_to_category(self):
        # given
        category = Category.objects.create(name="Category")
        self.app.set_user(self.user)
        page = self.app.get(reverse("aa_forum:admin_index"))
        # when
        form = page.forms[f"aa-forum-form-admin-add-board-{category.id}"]
        form[f"new-board-in-category-{category.id}-name"] = "Board"
        page = form.submit().follow()
        # then
        self.assertTemplateUsed(page, "aa_forum/view/administration/index.html")
        new_board = category.boards.last()
        self.assertEqual(new_board.name, "Board")

    def test_should_edit_board(self):
        # given
        category = Category.objects.create(name="Category")
        board = Board.objects.create(name="Board", category=category)
        self.app.set_user(self.user)
        page = self.app.get(reverse("aa_forum:admin_index"))
        # when
        form = page.forms[f"aa-forum-form-edit-board-{board.pk}"]
        form[f"edit-board-{board.pk}-name"] = "Dummy"
        page = form.submit().follow()
        # then
        self.assertTemplateUsed(page, "aa_forum/view/administration/index.html")
        board.refresh_from_db()
        self.assertEqual(board.name, "Dummy")

# Standard Library
from unittest.mock import patch

# Django
from django.contrib.auth.models import Group
from django.contrib.messages import get_messages
from django.test import TestCase
from django.urls import reverse

# AA Forum
from aa_forum.models import Board, Category, LastMessageSeen, Message, Topic
from aa_forum.tests.utils import create_fake_messages, create_fake_user, my_get_setting

VIEWS_PATH = "aa_forum.views.forum"


class TestIndexViews(TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        cls.user_1001 = create_fake_user(
            1001, "Bruce Wayne", permissions=["aa_forum.basic_access"]
        )
        cls.user_1002 = create_fake_user(
            1002, "Peter Parker", permissions=["aa_forum.basic_access"]
        )
        cls.category = Category.objects.create(name="Science")

    def setUp(self) -> None:
        # board 1 has an unread topic
        self.board_1 = Board.objects.create(name="Physics", category=self.category)
        topic_1 = Topic.objects.create(subject="Mysteries", board=self.board_1)
        create_fake_messages(topic_1, 4)
        topic_2 = Topic.objects.create(subject="Recent Discoveries", board=self.board_1)
        create_fake_messages(topic_2, 2)
        LastMessageSeen.objects.create(
            topic=topic_2,
            user=self.user_1001,
            message_time=topic_2.messages.order_by("-time_posted")[0].time_posted,
        )

        # board 2 has no unread topics
        self.board_2 = Board.objects.create(name="Math", category=self.category)
        topic = Topic.objects.create(subject="Unsolved Problems", board=self.board_2)
        create_fake_messages(topic, 2)
        LastMessageSeen.objects.create(
            topic=topic,
            user=self.user_1001,
            message_time=topic.messages.order_by("-time_posted")[0].time_posted,
        )

    def test_should_show_index(self):
        # given
        self.client.force_login(self.user_1001)
        # when
        res = self.client.get(reverse("aa_forum:forum_index"))
        # then
        self.assertEqual(res.status_code, 200)

    def test_should_show_new_indicator_when_one_topic_not_seen_yet(self):
        # given
        self.client.force_login(self.user_1001)
        # when
        res = self.client.get(reverse("aa_forum:forum_index"))
        # then
        self.assertEqual(res.status_code, 200)
        self.assertContains(res, f"aa-forum-link-on-{self.board_1.id}")
        self.assertNotContains(res, f"aa-forum-link-on-{self.board_2.id}")

    def test_should_show_new_indicator_when_new_posts_are_made(self):
        # given
        self.client.force_login(self.user_1001)
        # when
        Message.objects.create(
            topic=self.board_2.topics.first(),
            user_created=self.user_1002,
            message="new message",
        )
        res = self.client.get(reverse("aa_forum:forum_index"))
        # then
        self.assertEqual(res.status_code, 200)
        self.assertContains(res, f"aa-forum-link-on-{self.board_2.id}")

    def test_should_show_counts(self):
        # given
        self.client.force_login(self.user_1001)
        # when
        res = self.client.get(reverse("aa_forum:forum_index"))
        # then
        self.assertEqual(res.status_code, 200)
        self.assertContains(res, "6 Posts")
        self.assertContains(res, "2 Topics")

    def test_should_show_empty_counts_after_all_topics_are_deleted(self):
        # given
        Topic.objects.all().delete()
        self.client.force_login(self.user_1001)
        # when
        res = self.client.get(reverse("aa_forum:forum_index"))
        # then
        self.assertEqual(res.status_code, 200)
        self.assertContains(res, "0 Posts")
        self.assertContains(res, "0 Topics")


class TestIndexViewsSpecial(TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        cls.user_1001 = create_fake_user(
            1001, "Bruce Wayne", permissions=["aa_forum.basic_access"]
        )
        cls.user_1002 = create_fake_user(
            1002, "Peter Parker", permissions=["aa_forum.basic_access"]
        )
        cls.category = Category.objects.create(name="Science")

    def test_should_show_empty_counts_after_all_topics_are_deleted_with_child_board(
        self,
    ):
        # given
        board = Board.objects.create(name="Physics", category=self.category)
        topic = Topic.objects.create(subject="alpha", board=board)
        create_fake_messages(topic, 1)
        child_board = Board.objects.create(
            name="Thermodynamics", category=self.category, parent_board=board
        )
        child_topic = Topic.objects.create(subject="bravo", board=child_board)
        create_fake_messages(child_topic, 1)
        child_topic.delete()
        self.client.force_login(self.user_1001)
        # when
        res = self.client.get(reverse("aa_forum:forum_index"))
        # then
        self.assertEqual(res.status_code, 200)
        self.assertContains(res, "1 Posts")
        self.assertContains(res, "1 Topics")


class TestBoardViews(TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        cls.user_1001 = create_fake_user(
            1001, "Bruce Wayne", permissions=["aa_forum.basic_access"]
        )
        cls.user_1002 = create_fake_user(
            1002, "Peter Parker", permissions=["aa_forum.basic_access"]
        )
        cls.user_1003 = create_fake_user(
            1003,
            "Clark Kent",
            permissions=["aa_forum.basic_access", "aa_forum.manage_forum"],
        )
        cls.category = Category.objects.create(name="Science")
        cls.board = Board.objects.create(name="Physics", category=cls.category)

    def setUp(self) -> None:
        # topic 1 is completely new
        self.topic_1 = Topic.objects.create(subject="Mysteries", board=self.board)
        create_fake_messages(self.topic_1, 15)
        # topic 2 is read
        self.topic_2 = Topic.objects.create(subject="Off Topic", board=self.board)
        create_fake_messages(self.topic_2, 9)
        LastMessageSeen.objects.create(
            topic=self.topic_2,
            user=self.user_1001,
            message_time=self.topic_2.messages.order_by("-time_posted")[0].time_posted,
        )

    def test_should_show_new_indicator_when_topic_not_seen_yet(self):
        # given
        self.client.force_login(self.user_1001)
        # when
        res = self.client.get(
            reverse("aa_forum:forum_board", args=[self.category.slug, self.board.slug])
        )
        # then
        self.assertEqual(res.status_code, 200)
        self.assertContains(res, f"aa-forum-link-new-{self.topic_1.id}")

    def test_should_show_new_indicator_when_seen_first_page_only(self):
        # given
        self.client.force_login(self.user_1001)
        last_message_seen = self.topic_1.messages.order_by("time_posted")[4]
        LastMessageSeen.objects.create(
            topic=self.topic_1,
            user=self.user_1001,
            message_time=last_message_seen.time_posted,
        )
        # when
        res = self.client.get(
            reverse("aa_forum:forum_board", args=[self.category.slug, self.board.slug])
        )
        # then
        self.assertEqual(res.status_code, 200)
        self.assertContains(res, f"aa-forum-link-new-{self.topic_1.id}")

    def test_should_show_new_indicator_when_seen_second_page_only(self):
        # given
        self.client.force_login(self.user_1001)
        last_message_seen = self.topic_1.messages.order_by("time_posted")[9]
        LastMessageSeen.objects.create(
            topic=self.topic_1,
            user=self.user_1001,
            message_time=last_message_seen.time_posted,
        )
        # when
        res = self.client.get(
            reverse("aa_forum:forum_board", args=[self.category.slug, self.board.slug])
        )
        # then
        self.assertEqual(res.status_code, 200)
        self.assertContains(res, f"aa-forum-link-new-{self.topic_1.id}")

    def test_should_not_show_new_indicator_when_seen_last_page(self):
        # given
        self.client.force_login(self.user_1001)
        last_message_seen = self.topic_1.messages.order_by("time_posted")[14]
        LastMessageSeen.objects.create(
            topic=self.topic_1,
            user=self.user_1001,
            message_time=last_message_seen.time_posted,
        )
        # when
        res = self.client.get(
            reverse("aa_forum:forum_board", args=[self.category.slug, self.board.slug])
        )
        # then
        self.assertEqual(res.status_code, 200)
        self.assertNotContains(res, f"aa-forum-link-new-{self.topic_1.id}")

    def test_should_show_new_indicator_when_new_posts_are_made(self):
        # given
        self.client.force_login(self.user_1001)
        # when
        Message.objects.create(
            topic=self.topic_2, user_created=self.user_1002, message="new message"
        )
        res = self.client.get(
            reverse("aa_forum:forum_board", args=[self.category.slug, self.board.slug])
        )
        # then
        self.assertEqual(res.status_code, 200)
        self.assertContains(res, f"aa-forum-link-new-{self.topic_2.id}")

    def test_should_delete_topic(self):
        # given
        self.client.force_login(self.user_1003)
        # when
        res = self.client.get(
            reverse("aa_forum:forum_topic_delete", args=[self.topic_1.pk])
        )
        # then
        self.assertRedirects(
            res,
            reverse(
                "aa_forum:forum_board", args=[self.board.category.slug, self.board.slug]
            ),
        )
        self.assertFalse(self.board.topics.filter(pk=self.topic_1.pk).exists())

    def test_should_return_404_when_delete_topic_not_found(self):
        # given
        self.client.force_login(self.user_1003)
        # when
        res = self.client.get(reverse("aa_forum:forum_topic_delete", args=[0]))
        # then
        self.assertEqual(res.status_code, 404)

    def test_should_lock_topic(self):
        # given
        self.client.force_login(self.user_1003)
        # when
        res = self.client.get(
            reverse("aa_forum:forum_topic_change_lock_state", args=[self.topic_1.pk])
        )
        # then
        self.assertRedirects(
            res,
            reverse(
                "aa_forum:forum_board", args=[self.board.category.slug, self.board.slug]
            ),
        )
        self.topic_1.refresh_from_db()
        self.assertTrue(self.topic_1.is_locked)

    def test_should_unlock_topic(self):
        # given
        self.client.force_login(self.user_1003)
        self.topic_1.is_locked = True
        self.topic_1.save()
        # when
        res = self.client.get(
            reverse("aa_forum:forum_topic_change_lock_state", args=[self.topic_1.pk])
        )
        # then
        self.assertRedirects(
            res,
            reverse(
                "aa_forum:forum_board", args=[self.board.category.slug, self.board.slug]
            ),
        )
        self.topic_1.refresh_from_db()
        self.assertFalse(self.topic_1.is_locked)

    def test_should_return_404_when_lock_topic_not_found(self):
        # given
        self.client.force_login(self.user_1003)
        # when
        res = self.client.get(
            reverse("aa_forum:forum_topic_change_lock_state", args=[0])
        )
        # then
        self.assertEqual(res.status_code, 404)

    def test_should_make_topic_sticky(self):
        # given
        self.client.force_login(self.user_1003)
        # when
        res = self.client.get(
            reverse("aa_forum:forum_topic_change_sticky_state", args=[self.topic_1.pk])
        )
        # then
        self.assertRedirects(
            res,
            reverse(
                "aa_forum:forum_board", args=[self.board.category.slug, self.board.slug]
            ),
        )
        self.topic_1.refresh_from_db()
        self.assertTrue(self.topic_1.is_sticky)

    def test_should_reverse_topic_sticky(self):
        # given
        self.client.force_login(self.user_1003)
        self.topic_1.is_sticky = True
        self.topic_1.save()
        # when
        res = self.client.get(
            reverse("aa_forum:forum_topic_change_sticky_state", args=[self.topic_1.pk])
        )
        # then
        self.assertRedirects(
            res,
            reverse(
                "aa_forum:forum_board", args=[self.board.category.slug, self.board.slug]
            ),
        )
        self.topic_1.refresh_from_db()
        self.assertFalse(self.topic_1.is_sticky)

    def test_should_return_404_when_sticky_topic_not_found(self):
        # given
        self.client.force_login(self.user_1003)
        # when
        res = self.client.get(
            reverse("aa_forum:forum_topic_change_sticky_state", args=[0])
        )
        # then
        self.assertEqual(res.status_code, 404)

    def test_should_return_board_does_not_exist_for_wrong_board_on_board_view(self):
        # given
        self.client.force_login(self.user_1001)

        # when
        response = self.client.get(
            reverse(
                "aa_forum:forum_board",
                args=["foo", "bar"],
            ),
        )

        # then
        messages = list(get_messages(response.wsgi_request))

        self.assertEqual(response.status_code, 302)
        self.assertRaises(Board.DoesNotExist)
        self.assertEqual(response.url, reverse("aa_forum:forum_index"))
        self.assertEqual(len(messages), 1)
        self.assertEqual(
            str(messages[0]),
            (
                "<h4>Error!</h4><p>The board you were trying to visit does "
                "either not exist, or you don't have access to it ...</p>"
            ),
        )

    def test_should_return_category_does_not_exists_on_new_topic(self):
        # given
        self.client.force_login(self.user_1001)

        # when
        response = self.client.get(
            reverse(
                "aa_forum:forum_board_new_topic",
                args=["foo", "bar"],
            ),
        )

        # then
        messages = list(get_messages(response.wsgi_request))

        self.assertEqual(response.status_code, 302)
        self.assertRaises(Category.DoesNotExist)
        self.assertEqual(response.url, reverse("aa_forum:forum_index"))
        self.assertEqual(len(messages), 1)
        self.assertEqual(
            str(messages[0]),
            (
                "<h4>Error!</h4><p>The category you were trying to post in does "
                "not exist ...</p>"
            ),
        )

    def test_should_return_board_does_not_exists_on_new_topic(self):
        # given
        self.client.force_login(self.user_1001)

        # when
        response = self.client.get(
            reverse(
                "aa_forum:forum_board_new_topic",
                args=[self.category.slug, "bar"],
            ),
        )

        # then
        messages = list(get_messages(response.wsgi_request))

        self.assertEqual(response.status_code, 302)
        self.assertRaises(Board.DoesNotExist)
        self.assertEqual(response.url, reverse("aa_forum:forum_index"))
        self.assertEqual(len(messages), 1)
        self.assertEqual(
            str(messages[0]),
            (
                "<h4>Error!</h4><p>The board you were trying to post in does "
                "either not exist, or you don't have access to it ...</p>"
            ),
        )


@patch(VIEWS_PATH + ".Setting.objects.get_setting", new=my_get_setting)
class TestTopicViews(TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        cls.user_1001 = create_fake_user(
            1001, "Bruce Wayne", permissions=["aa_forum.basic_access"]
        )
        cls.user_1003 = create_fake_user(
            1003,
            "Clark Lent",
            permissions=["aa_forum.basic_access", "aa_forum.manage_forum"],
        )
        cls.group = Group.objects.create(name="Superhero")
        cls.announcement_group = Group.objects.create(name="Justice League")

        cls.user_1004 = create_fake_user(
            1004, "Luke Skywalker", permissions=["aa_forum.basic_access"]
        )
        cls.user_1004.groups.add(cls.announcement_group)

    def setUp(self) -> None:
        self.category = Category.objects.create(name="Science")
        self.board = Board.objects.create(name="Physics", category=self.category)
        self.announcement_board = Board.objects.create(
            name="Chemistry", category=self.category, is_announcement_board=True
        )
        self.topic = Topic.objects.create(subject="Mysteries", board=self.board)
        create_fake_messages(self.topic, 15)

    def test_should_remember_last_message_seen_by_user_page_1(self):
        # given
        self.client.force_login(self.user_1001)
        # when
        res = self.client.get(
            reverse(
                "aa_forum:forum_topic",
                args=[self.category.slug, self.board.slug, self.topic.slug],
            )
        )
        # then
        self.assertEqual(res.status_code, 200)
        last_message_seen = LastMessageSeen.objects.get(
            topic=self.topic, user=self.user_1001
        )
        # view has 2 pages á 5 messages. this is last message on 1st page
        last_message = self.topic.messages.order_by("time_posted")[4]
        self.assertEqual(last_message_seen.message_time, last_message.time_posted)

    def test_should_remember_last_message_seen_by_user_page_2(self):
        # given
        self.client.force_login(self.user_1001)
        # when
        res = self.client.get(
            reverse(
                "aa_forum:forum_topic",
                args=[self.category.slug, self.board.slug, self.topic.slug, 2],
            )
        )
        # then
        self.assertEqual(res.status_code, 200)
        last_message_seen = LastMessageSeen.objects.get(
            topic=self.topic, user=self.user_1001
        )
        # view has 2 pages á 5 messages. this is last message on 2nd page
        last_message = Message.objects.order_by("time_posted")[9]
        self.assertEqual(last_message_seen.message_time, last_message.time_posted)

    def test_should_remember_last_message_seen_by_user_when_opening_previous_pages(
        self,
    ):
        # given
        self.client.force_login(self.user_1001)
        res = self.client.get(
            reverse(
                "aa_forum:forum_topic",
                args=[self.category.slug, self.board.slug, self.topic.slug, 2],
            )
        )
        # when
        res = self.client.get(
            reverse(
                "aa_forum:forum_topic",
                args=[self.category.slug, self.board.slug, self.topic.slug, 1],
            )
        )
        # then
        self.assertEqual(res.status_code, 200)
        last_message_seen = LastMessageSeen.objects.get(
            topic=self.topic, user=self.user_1001
        )
        # view has 2 pages á 5 messages. this is last message on 2nd page
        last_message = Message.objects.order_by("time_posted")[9]
        self.assertEqual(last_message_seen.message_time, last_message.time_posted)

    def test_should_redirect_to_first_message_when_topic_not_seen_yet(self):
        # given
        self.client.force_login(self.user_1001)
        first_message = self.topic.messages.order_by("time_posted").first()
        # when
        res = self.client.get(
            reverse(
                "aa_forum:forum_topic_first_unread_message",
                args=[self.category.slug, self.board.slug, self.topic.slug],
            )
        )
        # then
        self.assertRedirects(res, first_message.get_absolute_url())

    def test_should_redirect_to_first_new_message_normal(self):
        # given
        self.client.force_login(self.user_1001)
        messages_sorted = list(self.topic.messages.order_by("time_posted"))
        last_seen_message = messages_sorted[2]
        first_unseen_message = messages_sorted[3]
        LastMessageSeen.objects.create(
            topic=self.topic,
            user=self.user_1001,
            message_time=last_seen_message.time_posted,
        )
        # when
        res = self.client.get(
            reverse(
                "aa_forum:forum_topic_first_unread_message",
                args=[self.category.slug, self.board.slug, self.topic.slug],
            )
        )
        # then
        self.assertRedirects(res, first_unseen_message.get_absolute_url())

    def test_should_redirect_to_first_unseen_message_when_last_seen_message_deleted(
        self,
    ):
        # given
        self.client.force_login(self.user_1001)
        messages_sorted = list(self.topic.messages.order_by("time_posted"))
        last_seen_message = messages_sorted[2]
        first_unseen_message = messages_sorted[3]
        LastMessageSeen.objects.create(
            topic=self.topic,
            user=self.user_1001,
            message_time=last_seen_message.time_posted,
        )
        last_seen_message.delete()
        # when
        res = self.client.get(
            reverse(
                "aa_forum:forum_topic_first_unread_message",
                args=[self.category.slug, self.board.slug, self.topic.slug],
            )
        )
        # then
        self.assertRedirects(res, first_unseen_message.get_absolute_url())

    def test_should_redirect_to_newest_message_when_seen_full_topic(self):
        # given
        self.client.force_login(self.user_1001)
        last_seen_message = self.topic.messages.order_by("-time_posted")[0]
        LastMessageSeen.objects.create(
            topic=self.topic,
            user=self.user_1001,
            message_time=last_seen_message.time_posted,
        )
        # when
        res = self.client.get(
            reverse(
                "aa_forum:forum_topic_first_unread_message",
                args=[self.category.slug, self.board.slug, self.topic.slug],
            )
        )
        # then
        self.assertRedirects(res, last_seen_message.get_absolute_url())

    def test_should_redirect_to_message_by_id_first_page(self):
        # given
        self.client.force_login(self.user_1001)
        my_message = self.topic.messages.order_by("time_posted")[3]
        # when
        res = self.client.get(
            reverse(
                "aa_forum:forum_message",
                args=[
                    my_message.topic.board.category.slug,
                    my_message.topic.board.slug,
                    my_message.topic.slug,
                    my_message.pk,
                ],
            ),
        )
        # then
        self.assertRedirects(res, my_message.get_absolute_url())

    def test_should_redirect_to_message_by_id_middle_page_1(self):
        # given
        self.client.force_login(self.user_1001)
        my_message = self.topic.messages.order_by("time_posted")[5]
        # when
        res = self.client.get(
            reverse(
                "aa_forum:forum_message",
                args=[
                    my_message.topic.board.category.slug,
                    my_message.topic.board.slug,
                    my_message.topic.slug,
                    my_message.pk,
                ],
            ),
        )
        # then
        self.assertRedirects(res, my_message.get_absolute_url())

    def test_should_redirect_to_message_by_id_middle_page_2(self):
        # given
        self.client.force_login(self.user_1001)
        my_message = self.topic.messages.order_by("time_posted")[9]
        # when
        res = self.client.get(
            reverse(
                "aa_forum:forum_message",
                args=[
                    my_message.topic.board.category.slug,
                    my_message.topic.board.slug,
                    my_message.topic.slug,
                    my_message.pk,
                ],
            ),
        )
        # then
        self.assertRedirects(res, my_message.get_absolute_url())

    def test_should_redirect_to_message_by_id_last_page(self):
        # given
        self.client.force_login(self.user_1001)
        my_message = self.topic.messages.order_by("time_posted")[12]
        # when
        res = self.client.get(
            reverse(
                "aa_forum:forum_message",
                args=[
                    my_message.topic.board.category.slug,
                    my_message.topic.board.slug,
                    my_message.topic.slug,
                    my_message.pk,
                ],
            ),
        )
        # then
        self.assertRedirects(res, my_message.get_absolute_url())

    def test_should_delete_regular_message(self):
        # given
        self.client.force_login(self.user_1003)
        my_message = self.topic.messages.last()
        # when
        res = self.client.get(
            reverse("aa_forum:forum_message_delete", args=[my_message.pk])
        )
        # then
        self.assertEqual(res.status_code, 302)
        self.assertEqual(res.url, self.topic.get_absolute_url())
        self.assertFalse(self.topic.messages.filter(pk=my_message.pk).exists())

    def test_should_delete_first_message(self):
        # given
        self.client.force_login(self.user_1003)
        my_message = self.topic.messages.first()
        # when
        res = self.client.get(
            reverse("aa_forum:forum_message_delete", args=[my_message.pk])
        )
        # then
        self.assertEqual(res.status_code, 302)
        self.assertEqual(res.url, self.topic.board.get_absolute_url())
        self.assertFalse(self.topic.messages.filter(pk=my_message.pk).exists())
        self.assertFalse(self.board.topics.filter(pk=self.topic.pk).exists())

    def test_should_delete_last_message_in_topic(self):
        # given
        self.client.force_login(self.user_1003)
        my_message = self.topic.messages.first()
        self.topic.messages.exclude(pk=my_message.pk).delete()
        # when
        res = self.client.get(
            reverse("aa_forum:forum_message_delete", args=[my_message.pk])
        )
        # then
        self.assertEqual(res.status_code, 302)
        self.assertEqual(res.url, self.topic.board.get_absolute_url())
        self.assertFalse(self.topic.messages.filter(pk=my_message.pk).exists())
        self.assertFalse(self.board.topics.filter(pk=self.topic.pk).exists())

    def test_should_return_404_when_delete_message_not_found(self):
        # given
        self.client.force_login(self.user_1003)
        # when
        res = self.client.get(reverse("aa_forum:forum_message_delete", args=[0]))
        # then
        self.assertEqual(res.status_code, 404)

    @patch(VIEWS_PATH + ".messages")
    def test_should_not_edit_message_from_others(self, messages):
        # given
        self.client.force_login(self.user_1001)
        alien_message = Message.objects.create(
            topic=self.topic, user_created=self.user_1003, message="old text"
        )
        # when
        res = self.client.post(
            reverse(
                "aa_forum:forum_message_modify",
                args=[
                    self.category.slug,
                    self.board.slug,
                    self.topic.slug,
                    alien_message.pk,
                ],
            ),
            data={"message": "new text"},
        )
        # then
        self.assertEqual(res.status_code, 302)
        self.assertEqual(res.url, self.topic.get_absolute_url())
        alien_message.refresh_from_db()
        self.assertEqual(alien_message.message, "old text")
        self.assertTrue(messages.error.called)

    @patch(VIEWS_PATH + ".messages")
    def test_should_not_edit_message_from_board_with_no_access(self, messages):
        # given
        self.board.groups.add(self.group)
        self.client.force_login(self.user_1001)
        alien_message = Message.objects.create(
            topic=self.topic, user_created=self.user_1001, message="old text"
        )
        # when
        res = self.client.post(
            reverse(
                "aa_forum:forum_message_modify",
                args=[
                    self.category.slug,
                    self.board.slug,
                    self.topic.slug,
                    alien_message.pk,
                ],
            ),
            data={"message": "new text"},
        )
        # then
        self.assertEqual(res.status_code, 302)
        self.assertEqual(res.url, reverse("aa_forum:forum_index"))
        alien_message.refresh_from_db()
        self.assertEqual(alien_message.message, "old text")
        self.assertTrue(messages.error.called)

    def test_should_return_redirect_to_forum_index_if_topic_does_not_exist_on_topic_view(
        self,
    ):
        # given
        self.client.force_login(self.user_1001)

        # when
        response = self.client.get(
            reverse(
                "aa_forum:forum_topic",
                args=["foo", "bar", "foobar"],
            ),
        )

        # then
        messages = list(get_messages(response.wsgi_request))

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse("aa_forum:forum_index"))
        self.assertEqual(len(messages), 1)
        self.assertEqual(
            str(messages[0]),
            (
                "<h4>Error!</h4><p>The topic you were trying to view does not "
                "exist or you do not have access to it.</p>"
            ),
        )

    def test_should_return_redirect_to_forum_index_if_topic_does_not_exist_on_topic_modify_view(
        self,
    ):
        # given
        self.client.force_login(self.user_1001)

        # when
        response = self.client.get(
            reverse(
                "aa_forum:forum_topic_modify",
                args=["foo", "bar", "foobar"],
            ),
        )

        # then
        messages = list(get_messages(response.wsgi_request))

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse("aa_forum:forum_index"))
        self.assertEqual(len(messages), 1)
        self.assertEqual(
            str(messages[0]),
            (
                "<h4>Error!</h4><p>The topic you were trying to modify does not "
                "exist or you do not have access to it.</p>"
            ),
        )

    def test_should_return_redirect_to_forum_index_if_topic_does_not_exist_on_topic_reply(
        self,
    ):
        # given
        self.client.force_login(self.user_1001)

        # when
        response = self.client.get(
            reverse(
                "aa_forum:forum_topic_reply",
                args=["foo", "bar", "foobar"],
            ),
        )

        # then
        messages = list(get_messages(response.wsgi_request))

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse("aa_forum:forum_index"))
        self.assertEqual(len(messages), 1)
        self.assertEqual(
            str(messages[0]),
            (
                "<h4>Error!</h4><p>The topic you were trying to reply does not "
                "exist or you do not have access to it.</p>"
            ),
        )

    def test_should_return_redirect_to_forum_index_if_message_does_not_exist_on_message_view(
        self,
    ):
        # given
        self.client.force_login(self.user_1001)

        # when
        response = self.client.get(
            reverse(
                "aa_forum:forum_message",
                args=["foo", "bar", "foobar", 0],
            ),
        )

        # then
        messages = list(get_messages(response.wsgi_request))

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse("aa_forum:forum_index"))
        self.assertRaises(Message.DoesNotExist)
        self.assertEqual(len(messages), 1)
        self.assertEqual(
            str(messages[0]),
            "<h4>Error!</h4><p>The message doesn't exist ...</p>",
        )

    def test_should_show_all_unread_messages_view(self):
        # given
        self.client.force_login(self.user_1001)

        # when
        response = self.client.get(
            reverse("aa_forum:forum_topic_show_all_unread"),
        )

        # then
        self.assertEqual(response.status_code, 200)

    def test_should_return_to_forum_index_on_topic_modify_when_no_topic_found(self):
        # given
        self.client.force_login(self.user_1001)

        # when
        response = self.client.get(
            reverse(
                "aa_forum:forum_topic_modify",
                args=["foo", "bar", "foobar"],
            ),
        )

        # then
        messages = list(get_messages(response.wsgi_request))

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse("aa_forum:forum_index"))
        self.assertEqual(len(messages), 1)
        self.assertEqual(
            str(messages[0]),
            (
                "<h4>Error!</h4><p>The topic you were trying to modify does not "
                "exist or you do not have access to it.</p>"
            ),
        )

    def test_should_redirect_to_topic_view_for_user_without_rights_to_modify_topic(
        self,
    ):
        # given
        user_without_modify_perms = create_fake_user(
            1002, "Peter Parker", permissions=["aa_forum.basic_access"]
        )
        self.client.force_login(user_without_modify_perms)

        # when
        response = self.client.get(
            reverse(
                "aa_forum:forum_topic_modify",
                args=[self.category.slug, self.board.slug, self.topic.slug],
            ),
        )

        # then
        messages = list(get_messages(response.wsgi_request))

        self.assertEqual(response.status_code, 302)
        self.assertEqual(
            response.url,
            reverse(
                "aa_forum:forum_topic",
                args=[self.category.slug, self.board.slug, self.topic.slug],
            ),
        )
        self.assertEqual(len(messages), 1)
        self.assertEqual(
            str(messages[0]),
            "<h4>Error!</h4><p>You are not allowed to modify this topic!</p>",
        )

    def test_should_show_modify_topic_view(self):
        # given
        self.client.force_login(self.user_1003)

        # when
        response = self.client.get(
            reverse(
                "aa_forum:forum_topic_modify",
                args=[self.category.slug, self.board.slug, self.topic.slug],
            ),
        )

        # then
        self.assertEqual(response.status_code, 200)

    def test_can_create_new_topic_in_announcement_board_with_permission(self):
        # given
        self.client.force_login(self.user_1003)

        # when
        response = self.client.get(
            reverse(
                "aa_forum:forum_board_new_topic",
                args=[self.category.slug, self.announcement_board.slug],
            ),
        )

        # then
        self.assertEqual(response.status_code, 200)

    def test_can_create_new_topic_in_announcement_board_with_group(self):
        # given
        self.announcement_board.announcement_groups.add(self.announcement_group)
        self.client.force_login(self.user_1004)

        # when
        response = self.client.get(
            reverse(
                "aa_forum:forum_board_new_topic",
                args=[self.category.slug, self.announcement_board.slug],
            ),
        )

        # then
        self.assertEqual(response.status_code, 200)

    def test_cannot_create_new_topic_in_announcement_board_without_permission(self):
        # given
        self.client.force_login(self.user_1004)

        # when
        response = self.client.get(
            reverse(
                "aa_forum:forum_board_new_topic",
                args=[self.category.slug, self.announcement_board.slug],
            ),
        )

        messages = list(get_messages(response.wsgi_request))

        self.assertEqual(response.status_code, 302)
        self.assertEqual(
            response.url,
            reverse(
                "aa_forum:forum_board",
                args=[self.category.slug, self.announcement_board.slug],
            ),
        )
        self.assertEqual(len(messages), 1)
        self.assertEqual(
            str(messages[0]),
            (
                "<h4>Error!</h4><p>The board you were trying to post in is an "
                "Announcement Board and you don't have the permissions to start a "
                "topic there ...</p>"
            ),
        )

    def test_cannot_create_new_topic_in_announcement_board(self):
        # given
        self.client.force_login(self.user_1001)

        # when
        response = self.client.get(
            reverse(
                "aa_forum:forum_board_new_topic",
                args=[self.category.slug, self.announcement_board.slug],
            ),
        )

        messages = list(get_messages(response.wsgi_request))

        self.assertEqual(response.status_code, 302)
        self.assertEqual(
            response.url,
            reverse(
                "aa_forum:forum_board",
                args=[self.category.slug, self.announcement_board.slug],
            ),
        )
        self.assertEqual(len(messages), 1)
        self.assertEqual(
            str(messages[0]),
            (
                "<h4>Error!</h4><p>The board you were trying to post in is an "
                "Announcement Board and you don't have the permissions to start a "
                "topic there ...</p>"
            ),
        )

from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from django.contrib.auth import get_user_model
from posts.models import Post

User = get_user_model()

class PostAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='hamisi', password='pass123')

    def test_create_post_requires_auth(self):
        url = reverse('posts:post-list')
        res = self.client.post(url, {'title': 'T', 'content': 'C'}, format='json')
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_owner_can_edit_post(self):
        self.client.force_authenticate(user=self.user)
        url = reverse('posts:post-list')
        res = self.client.post(url, {'title': 'T', 'content': 'C'}, format='json')
        post_id = res.data['id']
        detail_url = reverse('posts:post-detail', args=[post_id])
        res2 = self.client.patch(detail_url, {'title': 'T2'}, format='json')
        self.assertEqual(res2.status_code, status.HTTP_200_OK)
        self.assertEqual(Post.objects.get(id=post_id).title, 'T2')
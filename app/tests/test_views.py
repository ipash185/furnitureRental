from django.test import TestCase, Client
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from django.contrib.auth.models import User
from app.models import Product, Comment
from ..views import *

class TestCommentViews(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='12345')
        image_file = SimpleUploadedFile("image.jpg", b"file_content", content_type="image/jpeg")
        self.product = Product.objects.create(name="Product 1", description="Description 1", brand="Brand 1", price=100.00, category="sofa", available=True, image=image_file)
        self.comment = Comment.objects.create(user=self.user, product=self.product, comment='Test comment')

    def test_view_comment(self):
        # Test viewing a comment detail
        response = self.client.get(reverse('product_detail', args=[self.product.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test comment')

    def test_delete_comment(self):
        # Test deleting a comment
        self.client.force_login(self.user)
        response = self.client.post(reverse('delete_comment', args=[self.comment.id]))
        self.assertEqual(response.status_code, 302)  # Assuming successful redirection
        self.assertFalse(Comment.objects.filter(comment='Test comment').exists())

    # Add more tests as needed

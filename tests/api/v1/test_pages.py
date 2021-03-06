#!/usr/bin/env python
# -*- coding: utf-8 -*-

from tests.helpers import *


def test_api_pages_get_non_admin():
    """Can a user get /api/v1/pages if not admin"""
    app = create_ctfd()
    with app.app_context():
        with app.test_client() as client:
            r = client.get('/api/v1/pages', json="")
            assert r.status_code == 403
    destroy_ctfd(app)


def test_api_pages_get_admin():
    """Can a user get /api/v1/pages if admin"""
    app = create_ctfd()
    with app.app_context():
        with login_as_user(app, 'admin') as client:
            r = client.get('/api/v1/pages', json="")
            assert r.status_code == 200
    destroy_ctfd(app)


def test_api_pages_post_non_admin():
    """Can a user post /api/v1/pages if not admin"""
    app = create_ctfd()
    with app.app_context():
        with app.test_client() as client:
            r = client.post('/api/v1/pages')
            assert r.status_code == 403
    destroy_ctfd(app)


def test_api_pages_post_admin():
    """Can a user post /api/v1/pages if admin"""
    app = create_ctfd()
    with app.app_context():
        gen_challenge(app.db)
        with login_as_user(app, name="admin") as client:
            with client.session_transaction() as sess:
                nonce = sess.get('nonce')
            r = client.post('/api/v1/pages', json={
                "title": "Title",
                "route": "/route",
                "content": "content",
                "id": "",
                "nonce": nonce,
                "auth_required": False})
            assert r.status_code == 200
    destroy_ctfd(app)


def test_api_page_get_non_admin():
    """Can a user get /api/v1/pages/<page_id> if not admin"""
    app = create_ctfd()
    with app.app_context():
        with app.test_client() as client:
            r = client.get('/api/v1/pages/2', json="")
            assert r.status_code == 403
    destroy_ctfd(app)


def test_api_page_get_admin():
    """Can a user get /api/v1/pages/<page_id> if admin"""
    app = create_ctfd()
    with app.app_context():
        gen_page(app.db, title="title", route="/route", content="content")
        with login_as_user(app, 'admin') as client:
            r = client.get('/api/v1/pages/2', json="")
            assert r.status_code == 200
    destroy_ctfd(app)


def test_api_page_patch_non_admin():
    """Can a user patch /api/v1/pages/<page_id> if not admin"""
    app = create_ctfd()
    with app.app_context():
        gen_page(app.db, title="title", route="/route", content="content")
        with app.test_client() as client:
            r = client.patch('/api/v1/pages/2', json="")
            assert r.status_code == 403
    destroy_ctfd(app)


def test_api_page_patch_admin():
    """Can a user patch /api/v1/pages/<page_id> if admin"""
    app = create_ctfd()
    with app.app_context():
        gen_page(app.db, title="title", route="/route", content="content")
        with login_as_user(app, 'admin') as client:
            with client.session_transaction() as sess:
                nonce = sess.get('nonce')
            r = client.patch('/api/v1/pages/2', json={
                "title": "Title",
                "route": "/route",
                "content": "content_edit",
                "id": "2",
                "nonce": nonce,
                "auth_required": False})
            assert r.status_code == 200
            assert r.get_json()['data']['content'] == "content_edit"
    destroy_ctfd(app)


def test_api_page_delete_non_admin():
    """Can a user delete /api/v1/pages/<page_id> if not admin"""
    app = create_ctfd()
    with app.app_context():
        gen_page(app.db, title="title", route="/route", content="content")
        with app.test_client() as client:
            r = client.delete('/api/v1/pages/2', json="")
            assert r.status_code == 403
    destroy_ctfd(app)


def test_api_page_delete_admin():
    """Can a user patch /api/v1/pages/<page_id> if admin"""
    app = create_ctfd()
    with app.app_context():
        gen_page(app.db, title="title", route="/route", content="content")
        with login_as_user(app, 'admin') as client:
            r = client.delete('/api/v1/pages/2', json="")
            assert r.status_code == 200
            assert r.get_json().get('data') is None
    destroy_ctfd(app)

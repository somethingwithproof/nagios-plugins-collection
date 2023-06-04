import pytest
from unittest.mock import patch, MagicMock
import urllib.error
import urllib.request
import xml.etree.ElementTree as ET
from main import check_reserved_prefixes, XMLError, URLConnectionError


@patch("urllib.request.urlopen")
@patch("xml.etree.ElementTree.fromstring")
def test_check_reserved_prefixes_found(urlopen_mock, fromstring_mock):
    content = "<root><reservedPrefixes>...</reservedPrefixes></root>"
    response_mock = MagicMock()
    response_mock.read.return_value = content.encode("utf-8")
    urlopen_mock.return_value = response_mock
    fromstring_mock.return_value.iter.return_value = ["<reservedPrefixes>...</reservedPrefixes>"]

    check_reserved_prefixes(url)

    assert urlopen_mock.call_args == ((url,),)
    assert fromstring_mock.call_args == ((content,),)
    assert response_mock.read.called
    assert "CHECK #2 OK - reservedPrefixes has been found." in pytest.stdout.getvalue()


@patch("urllib.request.urlopen")
@patch("xml.etree.ElementTree.fromstring")
def test_check_reserved_prefixes_not_found(urlopen_mock, fromstring_mock):
    content = "<root><otherElement>...</otherElement></root>"
    response_mock = MagicMock()
    response_mock.read.return_value = content.encode("utf-8")
    urlopen_mock.return_value = response_mock
    fromstring_mock.return_value.iter.return_value = ["<otherElement>...</otherElement>"]

    with pytest.raises(XMLError, match="reservedPrefixes not found."):
        check_reserved_prefixes(url)

    assert urlopen_mock.call_args == ((url,),)
    assert fromstring_mock.call_args == ((content,),)
    assert response_mock.read.called


@patch("urllib.request.urlopen")
def test_check_reserved_prefixes_url_error(urlopen_mock):
    urlopen_mock.side_effect = urllib.error.URLError("URL connection error")

    with pytest.raises(URLConnectionError, match="URL connection error"):
        check_reserved_prefixes(url)

    assert urlopen_mock.call_args == ((url,),)


@patch("urllib.request.urlopen")
@patch("xml.etree.ElementTree.fromstring")
def test_check_reserved_prefixes_xml_error(urlopen_mock, fromstring_mock):
    content = "<root><invalidXML</root>"
    response_mock = MagicMock()
    response_mock.read.return_value = content.encode("utf-8")
    urlopen_mock.return_value = response_mock
    fromstring_mock.side_effect = ET.ParseError("XML parsing error")

    with pytest.raises(XMLError, match="XML parsing error"):
        check_reserved_prefixes(url)

    assert urlopen_mock.call_args == ((url,),)
    assert fromstring_mock.call_args == ((content,),)
    assert response_mock.read.called

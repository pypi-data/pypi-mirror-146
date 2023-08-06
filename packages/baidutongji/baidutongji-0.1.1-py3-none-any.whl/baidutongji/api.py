from typing import Optional
import datetime
import requests

from .metrics import *
from .data import *


__all__ = ['refreshAccessToken', 'getSiteList', 'getTimeTrendRpt', 'getDistrictRpt', 'getCommonTrackRpt', 'getTrendTime', 'getTrendLatest', 'getSourceAll', 'getSourceEngine', 'getSourceSearchword', 'getSourceLink', 'getVisitToppage', 'getVisitLandingpage', 'getVisitTopdomain', 'getVisitDistrict', 'getVisitWorld']


GET_TOKEN_URL = 'https://openapi.baidu.com/oauth/2.0/token'
GET_SITE_LIST_URL = 'https://openapi.baidu.com/rest/2.0/tongji/config/getSiteList'
GET_REPORT_DATA_URL = 'https://openapi.baidu.com/rest/2.0/tongji/report/getData'


def cleanParams(params: dict) -> dict:
	"""
	清理参数
	:param params:
	:return:
	"""
	pop_key = []
	for key, value in params.items():
		if value is None or value == '':
			pop_key.append(key)
	for key in pop_key:
		params.pop(key)
	return params


def refreshAccessToken(client_id, client_secret, refresh_token) -> dict:
	"""
	刷新 access_token
	:param refresh_token:
	:return:
	"""
	params = {
		'refresh_token': refresh_token,
		'client_id': client_id,
		'client_secret': client_secret,
		'grant_type': 'refresh_token'
	}
	response = requests.get(GET_TOKEN_URL, params=cleanParams(params))
	return response.json()


def getSiteList(access_token) -> dict:
	"""
	获取站点列表
	:param access_token:
	:return:
	"""
	params = {
		'access_token': access_token
	}
	response = requests.get(GET_SITE_LIST_URL, params=cleanParams(params))
	return response.json()


def getTimeTrendRpt(access_token: str, site_id: str, start_date: datetime.date, end_date: datetime.date, metrics: TimeTrendRptMetrics) -> dict:
	"""
	获取网站概况（趋势数据）报表
	:param access_token:
	:param site_id:
	:param start_date:
	:param end_date:
	:param metrics:
	:return:
	"""
	params = {
		'access_token': access_token,
		'site_id': site_id,
		'start_date': start_date.strftime('%Y%m%d'),
		'end_date': end_date.strftime('%Y%m%d'),
		'metrics': metrics.getMetrics(),
		'method': 'overview/getTimeTrendRpt'
	}
	response = requests.get(GET_REPORT_DATA_URL, params=cleanParams(params))
	return response.json()


def getDistrictRpt(access_token: str, site_id: str, start_date: datetime.date, end_date: datetime.date, metrics: DistrictRptMetrics) -> dict:
	"""
	获取网站概况（地域分布）报表
	:param access_token:
	:param site_id:
	:param start_date:
	:param end_date:
	:param metrics:
	:return:
	"""
	params = {
		'access_token': access_token,
		'site_id': site_id,
		'start_date': start_date.strftime('%Y%m%d'),
		'end_date': end_date.strftime('%Y%m%d'),
		'metrics': metrics.getMetrics(),
		'method': 'overview/getDistrictRpt'
	}
	response = requests.get(GET_REPORT_DATA_URL, params=cleanParams(params))
	return response.json()


def getCommonTrackRpt(access_token: str, site_id: str, start_date: datetime.date, end_date: datetime.date, metrics: CommonTrackRptMetrics) -> dict:
	"""
	获取网站概况（来源网站、搜索词、入口页面、受访页面）报表
	:param access_token:
	:param site_id:
	:param start_date:
	:param end_date:
	:param metrics:
	:return:
	"""
	params = {
		'access_token': access_token,
		'site_id': site_id,
		'start_date': start_date.strftime('%Y%m%d'),
		'end_date': end_date.strftime('%Y%m%d'),
		'metrics': metrics.getMetrics(),
		'method': 'overview/getCommonTrackRpt'
	}
	response = requests.get(GET_REPORT_DATA_URL, params=cleanParams(params))
	return response.json()


def getTrendTime(access_token: str, site_id: str, start_date: datetime.date, end_date: datetime.date, metrics: TrendTimeMetrics, 
	start_date2: Optional[datetime.date], end_date2: Optional[datetime.date], 
	source: Optional[Source], clientDevice: Optional[ClientDevice], visitor: Optional[VisitorType], gran: Optional[TimeGran], area: Optional[Region]) -> dict:
	"""
	获取趋势分析报表
	:param access_token:
	:param site_id:
	:param start_date:
	:param end_date:
	:param metrics:
	:param start_date2:
	:param end_date2:
	:param source:
	:param clientDevice:
	:param visitor:
	:param gran:
	:param area:
	:return:
	"""
	params = {
		'access_token': access_token,
		'site_id': site_id,
		'start_date': start_date.strftime('%Y%m%d'),
		'end_date': end_date.strftime('%Y%m%d'),
		'metrics': metrics.getMetrics(),
		'method': 'trend/time/a'
	}
	if start_date2 is not None and end_date2 is not None:
		params['start_date2'] = start_date2.strftime('%Y%m%d')
		params['end_date2'] = end_date2.strftime('%Y%m%d')
	if source is not None:
		params['source'] = source.value
	if clientDevice is not None:
		params['clientDevice'] = clientDevice.value
	if visitor is not None:
		params['visitor'] = visitor.value
	if gran is not None:
		params['gran'] = gran.value
	if area is not None:
		params['area'] = area
	response = requests.get(GET_REPORT_DATA_URL, params=cleanParams(params))
	return response.json()


def getTrendLatest(access_token: str, site_id: str, metrics: TrendLatestMetrics, source: Optional[Source], clientDevice: Optional[ClientDevice], visitor: Optional[VisitorType], area: Optional[Region]) -> dict:
	"""
	获取实时访客报表
	:param access_token:
	:param site_id:
	:param metrics:
	:param source:
	:param clientDevice:
	:param visitor:
	:param area:
	:return:
	"""
	params = {
		'access_token': access_token,
		'site_id': site_id,
		'metrics': metrics.getMetrics(),
		'method': 'trend/latest/a'
	}
	if source is not None:
		params['source'] = source.value
	if clientDevice is not None:
		params['clientDevice'] = clientDevice.value
	if visitor is not None:
		params['visitor'] = visitor.value
	if area is not None:
		params['area'] = area
	response = requests.get(GET_REPORT_DATA_URL, params=cleanParams(params))
	return response.json()


def getSourceAll(access_token: str, site_id: str, metrics: SourceMetrics, 
	start_date2: Optional[datetime.date], end_date2: Optional[datetime.date], 
	visitor: Optional[VisitorType], clientDevice: Optional[ClientDevice]) -> dict:
	"""
	获取来源报表
	:param access_token:
	:param site_id:
	:param metrics:
	:param start_date2:
	:param end_date2:
	:param visitor:
	:param clientDevice:
	:return:
	"""
	params = {
		'access_token': access_token,
		'site_id': site_id,
		'metrics': metrics.getMetrics(),
		'method': 'source/all/a'
	}
	if start_date2 is not None and end_date2 is not None:
		params['start_date2'] = start_date2.strftime('%Y%m%d')
		params['end_date2'] = end_date2.strftime('%Y%m%d')
	if visitor is not None:
		params['visitor'] = visitor.value
	if clientDevice is not None:
		params['clientDevice'] = clientDevice.value
	response = requests.get(GET_REPORT_DATA_URL, params=cleanParams(params))
	return response.json()


def getSourceEngine(access_token: str, site_id: str, metrics: SourceMetrics,
	start_date2: Optional[datetime.date], end_date2: Optional[datetime.date], 
	visitor: Optional[VisitorType], clientDevice: Optional[ClientDevice], area: Optional[Region]) -> dict:
	"""
	获取搜索引擎报表
	:param access_token:
	:param site_id:
	:param metrics:
	:param start_date2:
	:param end_date2:
	:param visitor:
	:param clientDevice:
	:param area:
	:return:
	"""
	params = {
		'access_token': access_token,
		'site_id': site_id,
		'metrics': metrics.getMetrics(),
		'method': 'source/engine/a'
	}
	if start_date2 is not None and end_date2 is not None:
		params['start_date2'] = start_date2.strftime('%Y%m%d')
		params['end_date2'] = end_date2.strftime('%Y%m%d')
	if visitor is not None:
		params['visitor'] = visitor.value
	if clientDevice is not None:
		params['clientDevice'] = clientDevice.value
	if area is not None:
		params['area'] = area
	response = requests.get(GET_REPORT_DATA_URL, params=cleanParams(params))
	return response.json()


def getSourceSearchword(access_token: str, site_id: str, metrics: SourceMetrics,
	start_date2: Optional[datetime.date], end_date2: Optional[datetime.date], 
	visitor: Optional[VisitorType], clientDevice: Optional[ClientDevice], source: Optional[Source]) -> dict:
	"""
	获取搜索词报表
	:param access_token:
	:param site_id:
	:param metrics:
	:param start_date2:
	:param end_date2:
	:param visitor:
	:param clientDevice:
	:param source:
	:return:
	"""
	params = {
		'access_token': access_token,
		'site_id': site_id,
		'metrics': metrics.getMetrics(),
		'method': 'source/searchword/a'
	}
	if start_date2 is not None and end_date2 is not None:
		params['start_date2'] = start_date2.strftime('%Y%m%d')
		params['end_date2'] = end_date2.strftime('%Y%m%d')
	if visitor is not None:
		params['visitor'] = visitor.value
	if clientDevice is not None:
		params['clientDevice'] = clientDevice.value
	if source is not None:
		params['source'] = source.value
	response = requests.get(GET_REPORT_DATA_URL, params=cleanParams(params))
	return response.json()


def getSourceLink(access_token: str, site_id: str, metrics: SourceMetrics,
	start_date2: Optional[datetime.date], end_date2: Optional[datetime.date], 
	visitor: Optional[VisitorType], clientDevice: Optional[ClientDevice], domainType: Optional[DomainType]) -> dict:
	"""
	获取外部链接报表
	:param access_token:
	:param site_id:
	:param metrics:
	:param start_date2:
	:param end_date2:
	:param visitor:
	:param clientDevice:
	:param domainType:
	:return:
	"""
	params = {
		'access_token': access_token,
		'site_id': site_id,
		'metrics': metrics.getMetrics(),
		'method': 'source/link/a'
	}
	if start_date2 is not None and end_date2 is not None:
		params['start_date2'] = start_date2.strftime('%Y%m%d')
		params['end_date2'] = end_date2.strftime('%Y%m%d')
	if visitor is not None:
		params['visitor'] = visitor.value
	if clientDevice is not None:
		params['clientDevice'] = clientDevice.value
	if domainType is not None:
		params['domainType'] = domainType.value
	response = requests.get(GET_REPORT_DATA_URL, params=cleanParams(params))
	return response.json()


def getVisitToppage(access_token: str, site_id: str, metrics: VisitToppageMetrics,
	start_date2: Optional[datetime.date], end_date2: Optional[datetime.date], 
	source: Optional[Source], visitor: Optional[VisitorType]) -> dict:
	"""
	获取受访页面报表
	:param access_token:
	:param site_id:
	:param metrics:
	:param start_date2:
	:param end_date2:
	:param source:
	:param visitor:
	:return:
	"""
	params = {
		'access_token': access_token,
		'site_id': site_id,
		'metrics': metrics.getMetrics(),
		'method': 'visit/toppage/a'
	}
	if start_date2 is not None and end_date2 is not None:
		params['start_date2'] = start_date2.strftime('%Y%m%d')
		params['end_date2'] = end_date2.strftime('%Y%m%d')
	if source is not None:
		params['source'] = source.value
	if visitor is not None:
		params['visitor'] = visitor.value
	response = requests.get(GET_REPORT_DATA_URL, params=cleanParams(params))
	return response.json()


def getVisitLandingpage(access_token: str, site_id: str, metrics: VisitLandingpageMetrics,
	start_date2: Optional[datetime.date], end_date2: Optional[datetime.date]) -> dict:
	"""
	获取入口页面报表
	:param access_token:
	:param site_id:
	:param metrics:
	:param start_date2:
	:param end_date2:
	:return:
	"""
	params = {
		'access_token': access_token,
		'site_id': site_id,
		'metrics': metrics.getMetrics(),
		'method': 'visit/landingpage/a'
	}
	if start_date2 is not None and end_date2 is not None:
		params['start_date2'] = start_date2.strftime('%Y%m%d')
		params['end_date2'] = end_date2.strftime('%Y%m%d')
	response = requests.get(GET_REPORT_DATA_URL, params=cleanParams(params))
	return response.json()


def getVisitTopdomain(access_token: str, site_id: str, metrics: VisitTopdomainMetrics,
	start_date2: Optional[datetime.date], end_date2: Optional[datetime.date], 
	source: Optional[Source], visitor: Optional[VisitorType]) -> dict:
	"""
	获取受访域名报表
	:param access_token:
	:param site_id:
	:param metrics:
	:param start_date2:
	:param end_date2:
	:param source:
	:param visitor:
	:return:
	"""
	params = {
		'access_token': access_token,
		'site_id': site_id,
		'metrics': metrics.getMetrics(),
		'method': 'visit/topdomain/a'
	}
	if start_date2 is not None and end_date2 is not None:
		params['start_date2'] = start_date2.strftime('%Y%m%d')
		params['end_date2'] = end_date2.strftime('%Y%m%d')
	if source is not None:
		params['source'] = source.value
	if visitor is not None:
		params['visitor'] = visitor.value
	response = requests.get(GET_REPORT_DATA_URL, params=cleanParams(params))
	return response.json()


def getVisitDistrict(access_token: str, site_id: str, metrics: SourceMetrics,
	start_date2: Optional[datetime.date], end_date2: Optional[datetime.date], 
	source: Optional[Source], visitor: Optional[VisitorType]) -> dict:
	"""
	获取地区分布报表
	:param access_token:
	:param site_id:
	:param metrics:
	:param start_date2:
	:param end_date2:
	:param source:
	:param visitor:
	:return:
	"""
	params = {
		'access_token': access_token,
		'site_id': site_id,
		'metrics': metrics.getMetrics(),
		'method': 'visit/district/a'
	}
	if start_date2 is not None and end_date2 is not None:
		params['start_date2'] = start_date2.strftime('%Y%m%d')
		params['end_date2'] = end_date2.strftime('%Y%m%d')
	if source is not None:
		params['source'] = source.value
	if visitor is not None:
		params['visitor'] = visitor.value
	response = requests.get(GET_REPORT_DATA_URL, params=cleanParams(params))
	return response.json()

def getVisitWorld(access_token: str, site_id: str, metrics: SourceMetrics,
	start_date2: Optional[datetime.date], end_date2: Optional[datetime.date], 
	source: Optional[Source], visitor: Optional[VisitorType]) -> dict:
	"""
	获取地区分布（按国家）报表
	:param access_token:
	:param site_id:
	:param metrics:
	:param start_date2:
	:param end_date2:
	:param source:
	:param visitor:
	:return:
	"""
	params = {
		'access_token': access_token,
		'site_id': site_id,
		'metrics': metrics.getMetrics(),
		'method': 'visit/world/a'
	}
	if start_date2 is not None and end_date2 is not None:
		params['start_date2'] = start_date2.strftime('%Y%m%d')
		params['end_date2'] = end_date2.strftime('%Y%m%d')
	if source is not None:
		params['source'] = source.value
	if visitor is not None:
		params['visitor'] = visitor.value
	response = requests.get(GET_REPORT_DATA_URL, params=cleanParams(params))
	return response.json()

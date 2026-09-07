import pymysql
from pymysql.cursors import DictCursor
from pymysql.err import OperationalError
from contextlib import contextmanager
from typing import List, Dict, Any, Optional, Union
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class MySQLClient:
    """
    MySQL 客户端封装
    """

    def __init__(
            self,
            host: str = 'localhost',
            port: int = 3306,
            user: str = 'root',
            password: str = 'rootroot',
            database: str = 'demo',
            charset: str = 'utf8mb4'
    ):
        self.config = {
            'host': host,
            'port': port,
            'user': user,
            'password': password,
            'database': database,
            'charset': charset,
            'cursorclass': DictCursor,
            'autocommit': False
        }
        # 初始化时测试连接，配置错误立即报错
        self._test_connection()

    def _test_connection(self):
        """测试连接，失败时给出明确提示"""
        try:
            conn = pymysql.connect(**self.config)
            conn.close()
            logger.info(f"✅ MySQL 连接成功: {self.config['host']}:{self.config['port']}/{self.config['database']}")
        except OperationalError as e:
            code, msg = e.args
            error_tips = {
                1045: f"❌ 用户名或密码错误！请检查 user='{self.config['user']}', password='***'",
                1049: f"❌ 数据库不存在！请检查 database='{self.config['database']}'",
                2003: f"❌ 连接被拒绝！请检查 host='{self.config['host']}', port={self.config['port']}，确认 MySQL 服务已启动",
                1044: f"❌ 用户 '{self.config['user']}' 没有访问数据库 '{self.config['database']}' 的权限",
            }
            tip = error_tips.get(code, f"❌ MySQL 连接错误 [{code}]: {msg}")
            logger.error(tip)
            raise ConnectionError(tip) from e

    @contextmanager
    def _get_cursor(self, conn=None):
        if conn:
            cursor = conn.cursor()
            try:
                yield cursor
            finally:
                cursor.close()
        else:
            _conn = pymysql.connect(**self.config)
            cursor = _conn.cursor()
            try:
                yield cursor
                _conn.commit()
            except Exception as e:
                _conn.rollback()
                logger.error(f"SQL 执行失败，已回滚: {e}")
                raise
            finally:
                cursor.close()
                _conn.close()

    @contextmanager
    def transaction(self):
        conn = pymysql.connect(**self.config)
        try:
            yield conn
            conn.commit()
            logger.info("✅ 事务提交成功")
        except Exception as e:
            conn.rollback()
            logger.error(f"❌ 事务回滚: {e}")
            raise
        finally:
            conn.close()

    # ==================== 查 ====================
    def query(self, sql: str, params: Optional[tuple] = None, fetch_one: bool = False):
        with self._get_cursor() as cursor:
            cursor.execute(sql, params or ())
            return cursor.fetchone() if fetch_one else cursor.fetchall()

    def query_one(self, sql: str, params: Optional[tuple] = None):
        return self.query(sql, params, fetch_one=True)

    def query_value(self, sql: str, params: Optional[tuple] = None):
        result = self.query_one(sql, params)
        return list(result.values())[0] if result else None

    # ==================== 增 ====================
    def insert(self, table: str, data: Dict[str, Any], conn=None) -> int:
        columns = ', '.join(f"`{k}`" for k in data.keys())
        placeholders = ', '.join(['%s'] * len(data))
        sql = f"INSERT INTO `{table}` ({columns}) VALUES ({placeholders})"
        with self._get_cursor(conn) as cursor:
            cursor.execute(sql, tuple(data.values()))
            return cursor.lastrowid

    def batch_insert(self, table: str, data_list: List[Dict[str, Any]], conn=None) -> int:
        if not data_list:
            return 0
        columns = ', '.join(f"`{k}`" for k in data_list[0].keys())
        placeholders = ', '.join(['%s'] * len(data_list[0]))
        sql = f"INSERT INTO `{table}` ({columns}) VALUES ({placeholders})"
        values = [tuple(d.values()) for d in data_list]
        with self._get_cursor(conn) as cursor:
            cursor.executemany(sql, values)
            return cursor.rowcount

    # ==================== 删 ====================
    def delete(self, table: str, where: str, params: Optional[tuple] = None, conn=None) -> int:
        if not where or where.strip() == '':
            raise ValueError("删除必须带 WHERE 条件！")
        sql = f"DELETE FROM `{table}` WHERE {where}"
        with self._get_cursor(conn) as cursor:
            cursor.execute(sql, params or ())
            return cursor.rowcount

    # ==================== 改 ====================
    def update(self, table: str, data: Dict[str, Any], where: str, where_params: Optional[tuple] = None,
               conn=None) -> int:
        if not where or where.strip() == '':
            raise ValueError("更新必须带 WHERE 条件！")
        set_clause = ', '.join(f"`{k}` = %s" for k in data.keys())
        sql = f"UPDATE `{table}` SET {set_clause} WHERE {where}"
        params = tuple(data.values()) + (where_params or ())
        with self._get_cursor(conn) as cursor:
            cursor.execute(sql, params)
            return cursor.rowcount

    # ==================== 通用执行 ====================
    def execute(self, sql: str, params: Optional[tuple] = None, conn=None) -> int:
        with self._get_cursor(conn) as cursor:
            cursor.execute(sql, params or ())
            return cursor.rowcount

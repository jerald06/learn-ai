from mcp.server.fastmcp import FastMCP
from sqlalchemy import create_engine, text
import json

# Create MCP server
mcp = FastMCP("mysql-risk-server")

# MySQL connection - Update with your credentials
# Format: mysql+pymysql://username:password@localhost/database_name
engine = create_engine(
    "mysql+pymysql://root:Jerald%40123@localhost/sample"
)

@mcp.tool()
def get_user(userId: int) -> str:
    """Get user details by userId from MySQL database"""
    try:
        with engine.connect() as conn:
            result = conn.execute(
                text("SELECT * FROM users WHERE userId=:id"),
                {"id": userId}
            )
            
            row = result.fetchone()
            
            if not row:
                return json.dumps({"error": "User not found"})
            
            # Convert row to dictionary
            columns = result.keys()
            user_data = dict(zip(columns, row))
            
            return json.dumps(user_data, indent=2, default=str)
            
    except Exception as e:
        return json.dumps({"error": str(e)})

@mcp.tool()
def list_users() -> str:
    """Get all users from MySQL database"""
    try:
        with engine.connect() as conn:
            result = conn.execute(text("SELECT * FROM users"))
            
            rows = result.fetchall()
            columns = result.keys()
            
            users = []
            for row in rows:
                user_data = dict(zip(columns, row))
                users.append(user_data)
            
            return json.dumps(users, indent=2, default=str)
            
    except Exception as e:
        return json.dumps({"error": str(e)})

@mcp.tool()
def get_high_risk_users() -> str:
    """Get users with creditScore below 650"""
    try:
        with engine.connect() as conn:
            result = conn.execute(
                text("SELECT * FROM users WHERE creditScore < 650")
            )
            
            rows = result.fetchall()
            columns = result.keys()
            
            users = []
            for row in rows:
                user_data = dict(zip(columns, row))
                users.append(user_data)
            
            return json.dumps(users, indent=2, default=str)
            
    except Exception as e:
        return json.dumps({"error": str(e)})

@mcp.tool()
def get_users_with_multiple_loans() -> str:
    """Get users with more than 1 existing loan"""
    try:
        with engine.connect() as conn:
            result = conn.execute(
                text("SELECT * FROM users WHERE existingLoans > 1")
            )
            
            rows = result.fetchall()
            columns = result.keys()
            
            users = []
            for row in rows:
                user_data = dict(zip(columns, row))
                users.append(user_data)
            
            return json.dumps(users, indent=2, default=str)
            
    except Exception as e:
        return json.dumps({"error": str(e)})

if __name__ == "__main__":
    print("Starting MCP MySQL Server...")
    print("Available tools:")
    print("- get_user(userId)")
    print("- list_users()")
    print("- get_high_risk_users()")
    print("- get_users_with_multiple_loans()")
    mcp.run()

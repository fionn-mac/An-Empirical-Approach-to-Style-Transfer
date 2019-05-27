#include <bits/stdc++.h>
using namespace std;

#define ll long long
#define db long double
#define ii pair<int,int>
#define vi vector<int>
#define fi first
#define se second
#define sz(a) (int)(a).size()
#define all(a) (a).begin(),(a).end()
#define pb push_back
#define mp make_pair
#define FN(i, n) for (int i = 0; i < (int)(n); ++i)
#define FEN(i,n) for (int i = 1;i <= (int)(n); ++i)
#define rep(i,a,b) for(int i=a;i<b;i++)
#define repv(i,a,b) for(int i=b-1;i>=a;i--)
#define SET(A, val) memset(A, val, sizeof(A))
// order_of_key (val): returns the no. of values less than val
// find_by_order (k): returns the kth largest element.(0-based)
#define TRACE
#ifdef TRACE
#define trace(...) __f(#__VA_ARGS__, __VA_ARGS__)
template <typename Arg1>
void __f(const char* name, Arg1&& arg1){
	cerr << name << " : " << arg1 << std::endl;
}
template <typename Arg1, typename... Args>
void __f(const char* names, Arg1&& arg1, Args&&... args){
	const char* comma = strchr(names + 1, ','); cerr.write(names, comma - names) << " : " << arg1<<" | ";__f(comma+1, args...);
}
#else
#define trace(...)
#endif

struct ahocorasick
{//SZ:no of nodes
	vi sufflink; int SZ;
	vector<map<char,int> > trie;//call findnextstate
	vector<string> strs;
	vector<int> cnt,match;
	vector<vi> tree;
	ahocorasick()
	{
		SZ=0;
		trie.resize(1);
		match.resize(1);
		match[0]=-1;
	}
	void insert(string &s)
	{
		int curr=0;//clear to reinit
		rep(i,0,sz(s))
		{
			if(!trie[curr].count(s[i]))
			{
				trie[curr][s[i]]=++SZ;
				trie.pb(map<char,int>());
				match.pb(-1);
			}
			curr=trie[curr][s[i]];
		}
		match[curr]=sz(strs);
		strs.pb(s);
	}
	void build_automation()
	{
		sufflink.resize(SZ+3);
		//tree.resize(SZ+3);
		//cnt.resize(SZ+3,0);
		queue<int> q;
		for(auto x:trie[0])
		{
			sufflink[x.se]=0;
			q.push(x.se);
		}
		while(!q.empty())
		{
			int curr=q.front();
			q.pop();
			for(auto x:trie[curr])
			{
				q.push(x.se);
				int tmp=sufflink[curr];
				while(!trie[tmp].count(x.fi) && tmp)
					tmp=sufflink[tmp];
				if(trie[tmp].count(x.fi))
					sufflink[x.se]=trie[tmp][x.fi];
				else
					sufflink[x.se]=0;
				if(sufflink[x.se]!=x.se)
				{
					if(match[x.se]==-1) match[x.se]=match[sufflink[x.se]];
					else if(match[sufflink[x.se]]!=-1)
					{
						if(sz(strs[match[sufflink[x.se]]])>sz(strs[match[x.se]]))
							match[x.se]=match[sufflink[x.se]];
					}
				}
			}
		}
	}
	int findnextstate(int curr,char ch)
	{
		while(curr && !trie[curr].count(ch)) curr=sufflink[curr];
		return (!trie[curr].count(ch))?0:trie[curr][ch];
	}
	vi query(string &s)
	{
		vi ret;
		ret.resize(sz(s));
		int ans=0; int curr=0;
		rep(i,0,sz(s))
		{
			curr=findnextstate(curr,s[i]);
			ret[i]=match[curr];
			if(match[curr]!=-1) curr=0;
		}
		return ret;
	}
	void clear()
	{
		trie.clear(); sufflink.clear();
		trie.resize(1); SZ=0;
	}
};
int main()
{
	ios_base::sync_with_stdio(false);
	cin.tie(0);
	cout.tie(0);
	int m;
	cin>>m;
	ahocorasick ac;
	rep(i,0,m+1)
	{
    string s;
    getline(cin, s);
    if (s.length() == 0) {
      continue;
    }
		ac.insert(s);
	}
	ac.build_automation();
	int t;
	cin>>t;
  t++;
	while(t--)
	{
    string s;
    getline(cin, s);
    if (s.length() == 0) {
      continue;
    }
		vi ret=ac.query(s);
		for(auto it:ret) cout<<it<<" ";
		cout<<endl;
	}
	return 0;
}

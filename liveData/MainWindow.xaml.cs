using System;
using System.Collections.Generic;
using System.Linq;
using System.Net.Http;
using System.Text;
using System.Threading.Tasks;
using System.Windows;
using System.Windows.Controls;
using System.Windows.Data;
using System.Windows.Documents;
using System.Windows.Input;
using System.Windows.Media;
using System.Windows.Media.Imaging;
using System.Windows.Navigation;
using System.Windows.Shapes;
using System.IO;
using System.Diagnostics;
using System.Net.Http.Headers;
using Newtonsoft.Json;

namespace LiveData

{
    /// <summary>
    /// Interaction logic for MainWindow.xaml
    /// </summary>
    public partial class MainWindow : Window
    {
        static HttpClient client = new HttpClient();

        public static string apikey = "";
        public static string password = "";
        public static string user_id = "";
        public static string account_number = "";

        public MainWindow()
        {
            InitializeComponent();
        }

        private async void Balance_Reload(object sender, RoutedEventArgs e)
        {
            var access_token = File.ReadAllText(@"C:\Users\Vinay\Desktop\tradealgo\getData\access_token.txt", Encoding.UTF8);
            var bearer_key = "Bearer " + access_token;
            client.DefaultRequestHeaders.Clear();
            client.DefaultRequestHeaders.Add("Authorization", bearer_key);
            var content = await client.GetAsync("https://api.tdameritrade.com/v1/accounts");
            if (content.StatusCode == System.Net.HttpStatusCode.Unauthorized)
            {
                var process = new Process();
                process.StartInfo.FileName = @"C:\Users\Vinay\Desktop\tradealgo\getData\getTokenDirect.py";
                process.Start();
                process.WaitForExit();

                client.DefaultRequestHeaders.Clear();
                access_token = File.ReadAllText(@"C:\Users\Vinay\Desktop\tradealgo\getData\access_token.txt", Encoding.UTF8);
                bearer_key = "Bearer " + access_token;
                client.DefaultRequestHeaders.Add("Authorization", bearer_key);
                content = await client.GetAsync("https://api.tdameritrade.com/v1/accounts");
                //Console.WriteLine(content);
            }
            String urlContents = await content.Content.ReadAsStringAsync();
            dynamic s = JsonConvert.DeserializeObject(urlContents);
            string TotalBalance = (string)s[0]["securitiesAccount"]["currentBalances"]["liquidationValue"];
            string BuyingPower = (string)s[0]["securitiesAccount"]["currentBalances"]["cashAvailableForTrading"];
            string UnsettledFunds = (string)s[0]["securitiesAccount"]["currentBalances"]["unsettledCash"];

            Total_Balance.Text = TotalBalance;
            Buying_Power.Text = BuyingPower;
            Unsettled_Funds.Text = UnsettledFunds;
        }

        private async void PL_Reload(object sender, RoutedEventArgs e)
        {
            /*var access_token = File.ReadAllText(@"C:\Users\Vinay\Desktop\tradealgo\getData\access_token.txt", Encoding.UTF8);
            var bearer_key = "Bearer " + access_token;
            client.DefaultRequestHeaders.Clear();
            client.DefaultRequestHeaders.Add("Authorization", bearer_key);
            client.DefaultRequestHeaders.Add("Content-Type", "application/json");
            var content = await client.GetAsync("https://api.tdameritrade.com/v1/accounts?fields=positions");
            if (content.StatusCode == System.Net.HttpStatusCode.Unauthorized)
            {
                var process = new Process();
                process.StartInfo.FileName = @"C:\Users\Vinay\Desktop\tradealgo\getData\getTokenDirect.py";
                process.Start();
                process.WaitForExit();

                client.DefaultRequestHeaders.Clear();
                access_token = File.ReadAllText(@"C:\Users\Vinay\Desktop\tradealgo\getData\access_token.txt", Encoding.UTF8);
                bearer_key = "Bearer " + access_token;
                client.DefaultRequestHeaders.Add("Authorization", bearer_key);
                content = await client.GetAsync("https://api.tdameritrade.com/v1/accounts");
                //Console.WriteLine(content);
            }
            String urlContents = await content.Content.ReadAsStringAsync();
            dynamic s = JsonConvert.DeserializeObject(urlContents);

            Console.WriteLine(s);*/
        }
    }
};
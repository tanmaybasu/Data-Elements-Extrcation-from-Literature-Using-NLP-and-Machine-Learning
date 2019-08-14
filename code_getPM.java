import java.io.*;
import java.util.*;
import java.util.regex.*;
import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.StringReader;
import java.net.MalformedURLException;
import java.net.URL;
import java.text.DateFormat;
import java.text.SimpleDateFormat;
import java.util.ArrayList;
import java.util.Calendar;
import java.util.Collections;
import java.util.Date;
import java.util.HashSet;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

class getPM {
    public static Pattern p_count = Pattern.compile("<Count>(\\d+)</Count>");
    public static Pattern p = Pattern.compile("<Id>(\\d+)</Id>");
    public static String prefix = "http://www.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?" +
	"db=pubmed&retmax=100000&retmode=xml&term=";
    public static void main(String args[])throws Exception{
	/*Date date = new Date();  
	DateFormat dateFormat = new SimpleDateFormat("yyyy/MM/dd");
	Calendar cal = Calendar.getInstance();
	cal.add(Calendar.DATE, -365*YEARS_BACK);
	fromDate = dateFormat.format(cal.getTime());
	toDate = dateFormat.format(date);*/
	BufferedReader br=new BufferedReader (new FileReader("titles.txt"));
	FileWriter fr=new FileWriter("out.txt");
	String s="";
	while((s=br.readLine())!=null){
	    ArrayList<String> out=getPmids(s);
	    for(int i=0;i<out.size();i++){
		fr.write(out.get(i).toString()+"\t");}
	    fr.write("\n");//fr.write("s+\n"); in you want to print the title as well.
	}
	br.close();fr.close();
    }
	
    public static ArrayList<String> getPmids(String query) {
	String fromDate="1978/01/01";String toDate="2015/10/18";
		String url = prefix+query.replaceAll("\\s+", "+")+"+AND+(\""+fromDate+"\"[PDat]:\""+toDate+"\"[PDat])";
		System.out.println(url);
		int count=-1;ArrayList<String> pmids=new ArrayList<String>();
		try {
			BufferedReader br = new BufferedReader(new InputStreamReader(new URL(url).openStream()));
			while(br.ready()){
				String line=br.readLine();
				//System.out.println(line);
				if(count<0){
					Matcher m = p_count.matcher(line);
					if(m.find()){
						count=Integer.parseInt(m.group(1));
						//System.out.println("count:"+count);
					}					
				}
				
				Matcher m = p.matcher(line);
				if(m.find()){
					pmids.add(m.group(1));
				}
					//
			}
			br.close();
		} catch (NumberFormatException e) {
			e.printStackTrace();
		} catch (MalformedURLException e) {
			e.printStackTrace();
		} catch (IOException e) {
			e.printStackTrace();
		}
		return pmids;
	}
}

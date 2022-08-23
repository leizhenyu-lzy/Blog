package testGson;

import com.google.gson.Gson;
import com.google.gson.GsonBuilder;

public class TestGson
{
    public static void main(String[] args)
    {
        Gson gson = new Gson();
        gson.serializeNulls();
        GsonBuilder gsonBuilder = new GsonBuilder();
    }
}

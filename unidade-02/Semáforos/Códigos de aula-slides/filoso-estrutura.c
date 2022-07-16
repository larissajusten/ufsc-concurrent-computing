while (1)
{
    pensa();
    if (i < N - 1)
    {
        pega(i);
        pega((i + 1) % N);
    }
    else
    {
        pega((i + 1) % N);
        pega(i);
    }
    come();
    devolve(i);
    devolve((i + 1) % N);
}

import Head from "next/head";
import styles from "../styles/Home.module.css";
import useSWR from "swr";
import Router from "next/router";

export default function Home({ backend_url }) {
  const { data, error } = useSWR(`${backend_url}/api/user`, fetch);

  if (!data) return <div>loading...</div>;

  if (error || data.status == 401) {
    Router.push("/login");
    return <p>Redirecting..</p>;
  }

  if (data.status == 200) {
    return (
      <div className={styles.container}>
        <Head>
          <title>Miljömätaren</title>
          <meta name="description" content="Miljömätaren" />
        </Head>

        <main className={styles.main}>
          <h1 className={styles.title}>Miljömätaren</h1>
        </main>

        <footer className={styles.footer}>
          <a
            href="https://github.com/vilhelmprytz/miljomataren"
            target="_blank"
            rel="noopener noreferrer"
          >
            github.com/vilhelmprytz/miljomataren
          </a>
        </footer>
      </div>
    );
  }
}

export async function getServerSideProps(context) {
  return {
    props: { backend_url: process.env.BACKEND_URL }, // will be passed to the page component as props
  };
}
